"""
User Management Service
Handles all user-related business logic
"""
from typing import Dict, Any, Optional
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.db import transaction
from django.core.exceptions import ValidationError
from App.models import Profile
from App.models_extended import HiringManager, CandidateProfile, RPOAdmin
from App.services.base_service import BaseService
from App.utils.response import ApiResponse
import logging

logger = logging.getLogger(__name__)


class UserService(BaseService):
    """Service for User operations"""
    
    model = User
    
    @classmethod
    @transaction.atomic
    def create_user(cls, username: str, email: str, password: str, 
                    role: str, **extra_data) -> Dict[str, Any]:
        """
        Create user with profile and role-specific data
        
        Args:
            username: Username
            email: Email address
            password: Password
            role: User role (candidate, hiring_manager, rpo_admin)
            extra_data: Additional user data
            
        Returns:
            ApiResponse dict
        """
        try:
            # Validate role
            if role not in ['candidate', 'hiring_manager', 'rpo_admin']:
                return ApiResponse.validation_error(
                    errors={'role': 'Invalid role specified'},
                    message="Invalid role"
                )
            
            # Check if user exists
            if User.objects.filter(username=username).exists():
                return ApiResponse.validation_error(
                    errors={'username': 'Username already exists'},
                    message="User already exists"
                )
            
            if User.objects.filter(email=email).exists():
                return ApiResponse.validation_error(
                    errors={'email': 'Email already exists'},
                    message="Email already exists"
                )
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=extra_data.get('first_name', ''),
                last_name=extra_data.get('last_name', '')
            )
            
            # Create profile
            profile = Profile.objects.create(
                user=user,
                role=role,
                full_name=extra_data.get('full_name', ''),
                phone=extra_data.get('phone', ''),
                work_status=extra_data.get('work_status', 'findjob'),
                email=email
            )
            
            # Add to group
            group_name = role.replace('_', ' ').title()
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
            
            # Create role-specific profile
            if role == 'candidate':
                CandidateProfile.objects.create(profile=profile)
            elif role == 'hiring_manager':
                if 'company_name' not in extra_data:
                    raise ValidationError({'company_name': 'Company name is required for hiring managers'})
                HiringManager.objects.create(
                    profile=profile,
                    company_name=extra_data['company_name']
                )
            elif role == 'rpo_admin':
                if 'organization_name' not in extra_data:
                    raise ValidationError({'organization_name': 'Organization name is required for RPO admins'})
                RPOAdmin.objects.create(
                    profile=profile,
                    organization_name=extra_data['organization_name']
                )
            
            return ApiResponse.created(
                data={
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': role,
                    'profile_id': profile.id
                },
                message="User created successfully"
            )
            
        except ValidationError as e:
            return ApiResponse.validation_error(
                errors=e.message_dict if hasattr(e, 'message_dict') else {'error': str(e)},
                message="Validation failed"
            )
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to create user",
                error_details=str(e)
            )
    
    @classmethod
    def authenticate_user(cls, username: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user and return user data
        
        Args:
            username: Username or email
            password: Password
            
        Returns:
            ApiResponse dict with user data
        """
        try:
            # Try to authenticate with username
            user = authenticate(username=username, password=password)
            
            # If failed, try with email
            if not user:
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if not user:
                return ApiResponse.unauthorized(
                    message="Invalid username or password"
                )
            
            if not user.is_active:
                return ApiResponse.forbidden(
                    message="Account is inactive"
                )
            
            # Get profile and role data
            try:
                profile = user.profile
                role_data = ProfileService.get_user_role_data(user)
                
                return ApiResponse.success(
                    data={
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'is_staff': user.is_staff,
                        },
                        'profile': {
                            'id': profile.id,
                            'role': profile.role,
                            'full_name': profile.full_name,
                            'phone': profile.phone,
                            'profile_image': profile.profile_image.url if profile.profile_image else None,
                        },
                        'role_data': role_data
                    },
                    message="Authentication successful"
                )
            except Profile.DoesNotExist:
                return ApiResponse.error(
                    message="User profile not found",
                    status_code=500
                )
                
        except Exception as e:
            logger.error(f"Error authenticating user: {str(e)}")
            return ApiResponse.server_error(
                message="Authentication failed",
                error_details=str(e)
            )
    
    @classmethod
    def get_user_by_username(cls, username: str) -> Dict[str, Any]:
        """Get user by username with profile data"""
        try:
            user = User.objects.select_related('profile').get(username=username)
            
            data = {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'profile': ProfileService.get_profile_by_user_id(user.id).get('data')
            }
            
            return ApiResponse.success(
                data=data,
                message="User retrieved successfully"
            )
        except User.DoesNotExist:
            return ApiResponse.not_found(
                message=f"User '{username}' not found"
            )
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to retrieve user",
                error_details=str(e)
            )


class ProfileService(BaseService):
    """Service for Profile operations"""
    
    model = Profile
    
    @classmethod
    def get_profile_by_user_id(cls, user_id: int) -> Dict[str, Any]:
        """Get profile by user ID with role-specific data"""
        try:
            profile = Profile.objects.select_related('user').get(user_id=user_id)
            
            data = {
                'id': profile.id,
                'user_id': profile.user_id,
                'full_name': profile.full_name,
                'phone': profile.phone,
                'role': profile.role,
                'work_status': profile.work_status,
                'job_title': profile.job_title,
                'age': profile.age,
                'about': profile.about,
                'email': profile.email,
                'address': profile.address,
                'profile_image': profile.profile_image.url if profile.profile_image else None,
                'resume': profile.resume.url if profile.resume else None,
                'profile_completion': profile.profile_completion,
            }
            
            # Add role-specific data
            role_data = cls.get_user_role_data(profile.user)
            if role_data:
                data['role_data'] = role_data
            
            return ApiResponse.success(
                data=data,
                message="Profile retrieved successfully"
            )
        except Profile.DoesNotExist:
            return ApiResponse.not_found(
                message=f"Profile for user ID {user_id} not found"
            )
        except Exception as e:
            logger.error(f"Error getting profile: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to retrieve profile",
                error_details=str(e)
            )
    
    @classmethod
    def update_profile(cls, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        try:
            profile = Profile.objects.get(user_id=user_id)
            
            # Update basic fields
            allowed_fields = [
                'full_name', 'phone', 'job_title', 'age', 'about',
                'email', 'address', 'address2', 'temp_address', 'zip_code',
                'languages', 'facebook', 'twitter', 'instagram', 'linkedin'
            ]
            
            for field in allowed_fields:
                if field in data:
                    setattr(profile, field, data[field])
            
            profile.save()
            
            return ApiResponse.success(
                data={'profile_id': profile.id},
                message="Profile updated successfully"
            )
        except Profile.DoesNotExist:
            return ApiResponse.not_found(
                message=f"Profile for user ID {user_id} not found"
            )
        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            return ApiResponse.server_error(
                message="Failed to update profile",
                error_details=str(e)
            )
    
    @classmethod
    def get_user_role_data(cls, user: User) -> Optional[Dict[str, Any]]:
        """Get role-specific data for user"""
        try:
            profile = user.profile
            
            if profile.role == 'candidate':
                try:
                    candidate = profile.candidate_data
                    return {
                        'current_job_title': candidate.current_job_title,
                        'current_company': candidate.current_company,
                        'expected_salary': float(candidate.expected_salary) if candidate.expected_salary else None,
                        'job_search_status': candidate.job_search_status,
                        'total_applications': candidate.total_applications,
                    }
                except CandidateProfile.DoesNotExist:
                    return None
                    
            elif profile.role == 'hiring_manager':
                try:
                    hm = profile.hiring_manager_data
                    return {
                        'company_name': hm.company_name,
                        'department': hm.department,
                        'position': hm.position,
                        'is_verified': hm.is_verified,
                        'total_jobs_posted': hm.total_jobs_posted,
                    }
                except HiringManager.DoesNotExist:
                    return None
                    
            elif profile.role == 'rpo_admin':
                try:
                    rpo = profile.rpo_admin_data
                    return {
                        'organization_name': rpo.organization_name,
                        'is_verified': rpo.is_verified,
                        'total_placements': rpo.total_placements,
                        'total_clients': rpo.total_clients,
                    }
                except RPOAdmin.DoesNotExist:
                    return None
                    
        except Profile.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error getting role data: {str(e)}")
            return None
