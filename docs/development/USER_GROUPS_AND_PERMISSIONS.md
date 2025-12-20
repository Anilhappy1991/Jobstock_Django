# User Groups and Permissions Documentation

## Overview

This document outlines the user groups, permissions, and role-based access control (RBAC) implementation for the Jobstock Django application. The system is designed to support AI-powered job requisition analysis and candidate matching with three primary user roles.

**Document Version:** 1.0  
**Last Updated:** December 20, 2025  
**Author:** System Administrator

---

## Table of Contents

1. [User Groups](#user-groups)
2. [User Stories and Requirements](#user-stories-and-requirements)
3. [Permissions Matrix](#permissions-matrix)
4. [User Credentials](#user-credentials)
5. [Setup Instructions](#setup-instructions)
6. [Security Considerations](#security-considerations)

---

## User Groups

The application implements three distinct user groups, each with specific permissions aligned with their functional responsibilities:

### 1. Hiring Manager

**Purpose:** Create and manage job postings, view candidate profiles

**Key Responsibilities:**
- Upload job descriptions (simple or detailed)
- Create job requisitions
- View AI-generated job profiles
- Review candidate profiles
- Monitor job posting status

**Access Level:** Limited - Job creation and candidate viewing only

### 2. RPO Admin (Recruitment Process Outsourcing Administrator)

**Purpose:** Full control over recruitment process with AI tuning capabilities

**Key Responsibilities:**
- Review and approve AI-generated job profiles
- Tune and calibrate job matching criteria
- Add or up-weight specific skills in job requirements
- Manage candidate profiles
- Access analytics and benchmarking data
- View time-to-fill estimates
- Review salary benchmarks

**Access Level:** Advanced - Full CRUD operations on jobs and profiles

### 3. System Admin

**Purpose:** Complete system administration and configuration

**Key Responsibilities:**
- Full system access
- User and group management
- System configuration
- Database administration
- All permissions across the platform

**Access Level:** Superuser - Complete system control

---

## User Stories and Requirements

### Hiring Manager User Stories

**Story 1: Simple Job Upload**
> As a Hiring Manager, I want to upload a simple job description (or even just a job title), so that the AI can analyze it and generate a detailed, structured job requisition and an ideal candidate profile.

**Acceptance Criteria:**
- Can create new job postings via Django admin or API
- Can upload job descriptions in various formats
- Can view AI-generated structured job requisitions
- Can review ideal candidate profiles

**Required Permissions:**
- `app.add_job` - Create new job postings
- `app.view_job` - View job details
- `app.change_job` - Edit job postings
- `app.view_profile` - View candidate profiles

---

### System (AI) User Stories

**Story 2: Automated Job Parsing**
> As a System, I want to parse the job description to automatically extract key skills, required experience, education level, and location, so that these become the core matching criteria.

**System Functionality:**
- Natural Language Processing (NLP) for job description analysis
- Automated skill extraction
- Experience level detection
- Education requirement parsing
- Location parsing
- Structured data generation

**Implementation Notes:**
- This functionality is handled by the system/backend
- No specific user permissions required
- Runs as automated background process

---

### RPO Admin User Stories

**Story 3: AI Profile Tuning**
> As an RPO Admin, I want to review the AI-generated "benchmark" job profile and "tune" it by adding or up-weighting specific skills, so that I can ensure the search is perfectly aligned with the client's needs.

**Acceptance Criteria:**
- Can view all AI-generated job profiles
- Can edit and adjust skill requirements
- Can add custom skills not detected by AI
- Can assign weight/priority to specific skills
- Can save and version profile configurations

**Required Permissions:**
- `app.add_job` - Create job postings
- `app.view_job` - View all jobs
- `app.change_job` - Modify job details
- `app.delete_job` - Remove jobs if needed
- `app.add_profile` - Create candidate profiles
- `app.view_profile` - View all profiles
- `app.change_profile` - Edit profiles
- `app.delete_profile` - Remove profiles

**Story 4: Market Analytics**
> As a System, I want to analyze the job requirements against market data, so that I can provide the RPO Admin with an estimated "time-to-fill" and "salary benchmark."

**System Functionality:**
- Market data analysis integration
- Time-to-fill estimation algorithms
- Salary benchmarking calculations
- Data visualization for RPO Admins

**Required Access:**
- RPO Admins have read access to analytics data
- System generates reports automatically
- Integration with external market data APIs

---

## Permissions Matrix

| Permission | Hiring Manager | RPO Admin | System Admin |
|------------|---------------|-----------|--------------|
| **Job Management** |
| Create Jobs | ✓ | ✓ | ✓ |
| View Jobs | ✓ | ✓ | ✓ |
| Edit Jobs | ✓ | ✓ | ✓ |
| Delete Jobs | ✗ | ✓ | ✓ |
| **Profile Management** |
| Create Profiles | ✗ | ✓ | ✓ |
| View Profiles | ✓ (limited) | ✓ | ✓ |
| Edit Profiles | ✗ | ✓ | ✓ |
| Delete Profiles | ✗ | ✓ | ✓ |
| **System Administration** |
| Manage Users | ✗ | ✗ | ✓ |
| Manage Groups | ✗ | ✗ | ✓ |
| System Settings | ✗ | ✗ | ✓ |
| View Analytics | ✗ | ✓ | ✓ |
| AI Tuning | ✗ | ✓ | ✓ |

### Detailed Permission Breakdown

#### Hiring Manager Group
```python
Permissions (4 total):
- app.add_job
- app.view_job
- app.change_job
- app.view_profile
```

#### RPO Admin Group
```python
Permissions (12 total):
- app.add_job
- app.view_job
- app.change_job
- app.delete_job
- app.add_profile
- app.view_profile
- app.change_profile
- app.delete_profile
- [Additional model permissions as configured]
```

#### System Admin Group
```python
Permissions (116+ total):
- ALL PERMISSIONS
- is_superuser: True
- Full Django admin access
```

---

## User Credentials

### Test/Development Users

> **⚠️ WARNING:** These credentials are for development/testing only. Change all passwords in production environments!

| Role | Username | Password | Email |
|------|----------|----------|-------|
| Hiring Manager | `hiring_manager` | `manager123` | hiring_manager@jobstock.com |
| RPO Admin | `rpo_admin` | `rpo123` | rpo_admin@jobstock.com |
| System Admin | `system_admin` | `admin123` | system_admin@jobstock.com |

### Login Access

All users have access to:
- Django Admin Panel: `http://localhost:8000/admin/`
- Application Dashboard: `http://localhost:8000/`

**Login Process:**
1. Navigate to the admin panel
2. Enter username and password
3. Access level is automatically determined by group membership

---

## Setup Instructions

### Automatic Setup (Recommended)

Use the provided management command to automatically create groups, assign permissions, and create test users:

```bash
python manage.py setup_groups_users
```

**What this command does:**
1. Creates three user groups (Hiring Manager, RPO Admin, System Admin)
2. Assigns appropriate permissions to each group
3. Creates test users for each group
4. Displays login credentials

### Manual Setup

If you need to manually create groups and users:

#### Step 1: Create Groups

```python
from django.contrib.auth.models import Group, Permission

# Create groups
hiring_manager_group = Group.objects.create(name='Hiring Manager')
rpo_admin_group = Group.objects.create(name='RPO Admin')
system_admin_group = Group.objects.create(name='System Admin')
```

#### Step 2: Assign Permissions

```python
from django.contrib.contenttypes.models import ContentType
from App.models import Job, Profile

# Hiring Manager permissions
job_ct = ContentType.objects.get_for_model(Job)
job_permissions = Permission.objects.filter(
    content_type=job_ct,
    codename__in=['add_job', 'view_job', 'change_job']
)
hiring_manager_group.permissions.add(*job_permissions)

profile_ct = ContentType.objects.get_for_model(Profile)
profile_view = Permission.objects.get(content_type=profile_ct, codename='view_profile')
hiring_manager_group.permissions.add(profile_view)

# RPO Admin permissions (full access to jobs and profiles)
rpo_admin_group.permissions.add(*Permission.objects.filter(content_type=job_ct))
rpo_admin_group.permissions.add(*Permission.objects.filter(content_type=profile_ct))

# System Admin permissions (all)
system_admin_group.permissions.add(*Permission.objects.all())
```

#### Step 3: Create Users

```python
from django.contrib.auth.models import User

# Hiring Manager
hm_user = User.objects.create_user(
    username='hiring_manager',
    email='hiring_manager@jobstock.com',
    password='manager123',
    first_name='John',
    last_name='Manager',
    is_staff=True
)
hm_user.groups.add(hiring_manager_group)

# RPO Admin
rpo_user = User.objects.create_user(
    username='rpo_admin',
    email='rpo_admin@jobstock.com',
    password='rpo123',
    first_name='Sarah',
    last_name='RPO',
    is_staff=True
)
rpo_user.groups.add(rpo_admin_group)

# System Admin
sys_user = User.objects.create_superuser(
    username='system_admin',
    email='system_admin@jobstock.com',
    password='admin123',
    first_name='Admin',
    last_name='System'
)
sys_user.groups.add(system_admin_group)
```

### Verifying Setup

To verify groups and permissions are correctly configured:

```bash
# Check groups
python manage.py shell
>>> from django.contrib.auth.models import Group
>>> for group in Group.objects.all():
...     print(f"{group.name}: {group.permissions.count()} permissions")

# Check users
>>> from django.contrib.auth.models import User
>>> for user in User.objects.filter(groups__isnull=False):
...     print(f"{user.username}: {list(user.groups.values_list('name', flat=True))}")
```

---

## Security Considerations

### Password Policy

**Development Environment:**
- Simple passwords for testing (`manager123`, `rpo123`, `admin123`)

**Production Environment:**
- Minimum 12 characters
- Must include uppercase, lowercase, numbers, and special characters
- Password expiration every 90 days
- No password reuse (last 5 passwords)
- Two-factor authentication (2FA) for RPO Admin and System Admin

### Access Control Best Practices

1. **Principle of Least Privilege**
   - Users only get permissions necessary for their role
   - Regular permission audits

2. **Group-Based Management**
   - Always assign permissions to groups, not individual users
   - Users inherit permissions from their group(s)

3. **Audit Logging**
   - Log all permission changes
   - Track user activities (especially RPO Admin tuning actions)
   - Monitor failed login attempts

4. **Session Management**
   - Session timeout: 30 minutes of inactivity
   - Secure session cookies (HTTPS only in production)
   - Session invalidation on password change

### Production Deployment Checklist

- [ ] Change all default passwords
- [ ] Enable HTTPS/SSL
- [ ] Configure SESSION_COOKIE_SECURE = True
- [ ] Configure CSRF_COOKIE_SECURE = True
- [ ] Set DEBUG = False
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Enable 2FA for admin users
- [ ] Set up password complexity requirements
- [ ] Configure audit logging
- [ ] Regular security updates
- [ ] Implement rate limiting for login attempts

---

## Future Enhancements

### Planned Features

1. **Candidate Group**
   - Self-service portal for candidates
   - Resume upload and profile management
   - Job application tracking

2. **Client Group**
   - Client company representatives
   - View their posted jobs
   - Access analytics for their positions

3. **Advanced Analytics Dashboard**
   - Custom reports for RPO Admins
   - Predictive analytics for time-to-fill
   - Market trend visualization

4. **API Access**
   - Role-based API authentication
   - JWT token support
   - Rate limiting per user group

5. **Workflow Automation**
   - Approval workflows for job postings
   - Automated notifications
   - Status tracking and escalations

---

## Support and Maintenance

### Regular Maintenance Tasks

**Daily:**
- Monitor failed login attempts
- Check system logs for errors

**Weekly:**
- Review user access logs
- Update user permissions as needed

**Monthly:**
- Audit group permissions
- Review and remove inactive users
- Update documentation

**Quarterly:**
- Security review
- Permission structure optimization
- User training and onboarding updates

### Getting Help

For issues with user groups and permissions:

1. Check this documentation first
2. Review Django admin logs
3. Contact system administrator
4. Raise a ticket in the issue tracker

---

## Appendix

### Related Documentation

- [Django Authentication System](https://docs.djangoproject.com/en/5.2/topics/auth/)
- [Django Permissions](https://docs.djangoproject.com/en/5.2/topics/auth/default/#permissions-and-authorization)
- [Project Organization](../../PROJECT_ORGANIZATION.md)
- [Code Refactoring Documentation](./CODE_REFACTORING_DOCUMENTATION.md)

### Management Commands

| Command | Purpose |
|---------|---------|
| `setup_groups_users` | Create groups, permissions, and test users |
| `createsuperuser` | Create a new superuser account |

### Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-12-20 | Initial documentation | System Admin |

---

**End of Document**
