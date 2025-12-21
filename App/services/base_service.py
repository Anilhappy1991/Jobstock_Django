"""
Base Service Layer
Provides foundation for all business logic services
"""
from typing import Dict, Any, Optional, List
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from App.utils.response import ApiResponse
import logging

logger = logging.getLogger(__name__)


class BaseService:
    """
    Base service class with common methods
    All service classes should inherit from this
    """
    
    model = None  # Override in child classes
    
    @classmethod
    def get_all(cls, filters: Optional[Dict] = None, order_by: str = '-created_at') -> Dict[str, Any]:
        """
        Get all records with optional filtering
        
        Args:
            filters: Dictionary of filter parameters
            order_by: Field to order by
            
        Returns:
            ApiResponse dict with queryset data
        """
        try:
            queryset = cls.model.objects.all()
            
            if filters:
                queryset = queryset.filter(**filters)
            
            if order_by:
                queryset = queryset.order_by(order_by)
            
            return ApiResponse.success(
                data={
                    'items': list(queryset.values()),
                    'count': queryset.count()
                },
                message=f"{cls.model.__name__} list retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error in {cls.__name__}.get_all: {str(e)}")
            return ApiResponse.server_error(
                message=f"Failed to retrieve {cls.model.__name__} list",
                error_details=str(e)
            )
    
    @classmethod
    def get_by_id(cls, id: int) -> Dict[str, Any]:
        """
        Get single record by ID
        
        Args:
            id: Record ID
            
        Returns:
            ApiResponse dict with record data
        """
        try:
            instance = cls.model.objects.get(id=id)
            return ApiResponse.success(
                data=cls._serialize_instance(instance),
                message=f"{cls.model.__name__} retrieved successfully"
            )
        except ObjectDoesNotExist:
            return ApiResponse.not_found(
                message=f"{cls.model.__name__} with ID {id} not found"
            )
        except Exception as e:
            logger.error(f"Error in {cls.__name__}.get_by_id: {str(e)}")
            return ApiResponse.server_error(
                message=f"Failed to retrieve {cls.model.__name__}",
                error_details=str(e)
            )
    
    @classmethod
    @transaction.atomic
    def create(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create new record
        
        Args:
            data: Dictionary of field values
            
        Returns:
            ApiResponse dict with created record
        """
        try:
            instance = cls.model.objects.create(**data)
            return ApiResponse.created(
                data=cls._serialize_instance(instance),
                message=f"{cls.model.__name__} created successfully"
            )
        except ValidationError as e:
            return ApiResponse.validation_error(
                errors=e.message_dict,
                message="Validation failed"
            )
        except Exception as e:
            logger.error(f"Error in {cls.__name__}.create: {str(e)}")
            return ApiResponse.server_error(
                message=f"Failed to create {cls.model.__name__}",
                error_details=str(e)
            )
    
    @classmethod
    @transaction.atomic
    def update(cls, id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update existing record
        
        Args:
            id: Record ID
            data: Dictionary of fields to update
            
        Returns:
            ApiResponse dict with updated record
        """
        try:
            instance = cls.model.objects.get(id=id)
            
            for key, value in data.items():
                setattr(instance, key, value)
            
            instance.full_clean()  # Validate
            instance.save()
            
            return ApiResponse.success(
                data=cls._serialize_instance(instance),
                message=f"{cls.model.__name__} updated successfully"
            )
        except ObjectDoesNotExist:
            return ApiResponse.not_found(
                message=f"{cls.model.__name__} with ID {id} not found"
            )
        except ValidationError as e:
            return ApiResponse.validation_error(
                errors=e.message_dict,
                message="Validation failed"
            )
        except Exception as e:
            logger.error(f"Error in {cls.__name__}.update: {str(e)}")
            return ApiResponse.server_error(
                message=f"Failed to update {cls.model.__name__}",
                error_details=str(e)
            )
    
    @classmethod
    @transaction.atomic
    def delete(cls, id: int) -> Dict[str, Any]:
        """
        Delete record
        
        Args:
            id: Record ID
            
        Returns:
            ApiResponse dict
        """
        try:
            instance = cls.model.objects.get(id=id)
            instance.delete()
            
            return ApiResponse.success(
                message=f"{cls.model.__name__} deleted successfully"
            )
        except ObjectDoesNotExist:
            return ApiResponse.not_found(
                message=f"{cls.model.__name__} with ID {id} not found"
            )
        except Exception as e:
            logger.error(f"Error in {cls.__name__}.delete: {str(e)}")
            return ApiResponse.server_error(
                message=f"Failed to delete {cls.model.__name__}",
                error_details=str(e)
            )
    
    @classmethod
    def _serialize_instance(cls, instance) -> Dict[str, Any]:
        """
        Serialize model instance to dictionary
        Override in child classes for custom serialization
        
        Args:
            instance: Model instance
            
        Returns:
            Dictionary of field values
        """
        # Basic serialization - override for complex models
        data = {}
        for field in instance._meta.fields:
            value = getattr(instance, field.name)
            if hasattr(value, 'isoformat'):  # DateTime
                data[field.name] = value.isoformat()
            elif hasattr(value, 'url'):  # File/Image
                data[field.name] = value.url if value else None
            else:
                data[field.name] = value
        return data
    
    @classmethod
    def paginate(cls, queryset, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Paginate queryset
        
        Args:
            queryset: QuerySet to paginate
            page: Page number
            page_size: Items per page
            
        Returns:
            Dictionary with paginated data
        """
        total_count = queryset.count()
        total_pages = (total_count + page_size - 1) // page_size
        
        start = (page - 1) * page_size
        end = start + page_size
        
        items = list(queryset[start:end].values())
        
        return {
            'items': items,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_previous': page > 1
            }
        }
