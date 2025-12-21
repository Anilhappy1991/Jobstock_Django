# Role-Based Dashboard Routing Implementation

## Overview
The system now automatically redirects users to their appropriate dashboard based on their role when they log in. Each user role sees their specific navigation menu and dashboard interface.

## Role-to-Dashboard Mapping

| User Role | Dashboard URL | Navigation Group | Description |
|-----------|---------------|------------------|-------------|
| **hiring_manager** | `/employer-dashboard/` | hiring_manager | Job posting, applicant management, interview scheduling |
| **rpo_admin** | `/employer-dashboard/` | rpo_admin | RPO admin functions (currently shares employer dashboard) |
| **candidate** | `/candidate-dashboard/` | candidate | Job search, applications, profile management |
| **superuser** | `/employer-dashboard/` | - | Full system access |
| **unknown** | `/` (index) | - | Default fallback for users without specific roles |

## Implementation Details

### 1. Login Flow (auth_views.py)
When a user logs in, the system:
1. Authenticates the user
2. Checks `user.profile.role` field
3. Falls back to checking `user.groups` if role is unknown
4. Redirects to appropriate dashboard

```python
# Role detection logic
user_role = 'unknown'
try:
    user_role = user.profile.role if hasattr(user, 'profile') else 'unknown'
except:
    pass

# Group-based fallback
if user_role == 'unknown':
    if user.groups.filter(name__in=['Hiring Managers', 'hiring_manager']).exists():
        user_role = 'hiring_manager'
    elif user.groups.filter(name='Candidates').exists():
        user_role = 'candidate'
    elif user.groups.filter(name='rpo_admin').exists():
        user_role = 'rpo_admin'

# Route to dashboard
if user_role == 'hiring_manager' or user.is_superuser:
    next_url = reverse('App:employer_dashboard')
elif user_role == 'candidate':
    next_url = reverse('App:candidate_dashboard')
elif user_role == 'rpo_admin':
    next_url = reverse('App:employer_dashboard')
else:
    next_url = reverse('App:index')
```

### 2. Dynamic Navigation System
Each dashboard displays navigation items from the database based on the user's role:

#### Navigation Service (services/navigation_service.py)
```python
def get_navigation_for_user(user):
    """Get navigation items for the current user based on their role"""
    try:
        user_role = user.profile.role if hasattr(user, 'profile') else 'unknown'
    except:
        user_role = 'unknown'
    
    # Filter groups by role
    groups = NavigationGroup.objects.filter(is_active=True)
    user_groups = []
    
    for group in groups:
        visible_roles = group.visible_to_roles or []
        if user_role in visible_roles or 'all' in visible_roles:
            user_groups.append(group)
    
    # Return formatted navigation data
    return ApiResponse.success(data={'groups': navigation_data})
```

#### Context Processor (context_processors_navigation.py)
Automatically injects navigation data into all templates:
```python
def navigation_processor(request):
    """Add navigation data to all templates"""
    if request.user.is_authenticated:
        response = NavigationService.get_navigation_for_user(request.user)
        if response.success:
            return response.data
    return {'navigation_groups': []}
```

### 3. Template Integration

#### For Hiring Managers (For-Employer/dashboard_nav.html)
```html
{% for group in navigation_groups %}
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" data-toggle="dropdown">
        <i class="{{ group.icon }}"></i>
        {{ group.name }}
        {% if group.badge_count %}<span class="badge">{{ group.badge_count }}</span>{% endif %}
    </a>
    <ul class="dropdown-menu">
        {% for item in group.items %}
        <li><a class="dropdown-item" href="{{ item.url }}">{{ item.name }}</a></li>
        {% endfor %}
    </ul>
</li>
{% endfor %}
```

#### For Candidates (For-Candidate/dashboard_nav.html)
Same MVT pattern as employer navigation, displays candidate-specific menu items.

## Current User Database

| Username | Role | Groups | Dashboard |
|----------|------|--------|-----------|
| rituranjangupta | hiring_manager | Hiring Managers, hiring_manager | employer_dashboard |
| hiring_manager | hiring_manager | hiring_manager | employer_dashboard |
| employer_test | hiring_manager | hiring_manager | employer_dashboard |
| rpo_admin | rpo_admin | rpo_admin | employer_dashboard |
| test | unknown | None | index |
| system_admin | unknown | System Admin | employer_dashboard (superuser) |

## Navigation Groups in Database

### 1. Candidate Navigation
- **visible_to_roles**: ["candidate"]
- **Items**: Job Search, My Applications, Profile, Messages, etc.

### 2. Hiring Manager Navigation
- **visible_to_roles**: ["hiring_manager"]
- **Items**: 
  - Job Management (Post New Job, Manage Jobs, Job Templates)
  - Applicant Tracking (Applications, Candidates, Shortlist)
  - Interview Management (Schedule, Calendar, Feedback)
  - Reports & Analytics
  - Settings

### 3. RPO Admin Navigation
- **visible_to_roles**: ["rpo_admin"]
- **Items**: Currently uses employer dashboard with potential for custom items

## Testing Role-Based Routing

### Test Script (test_role_routing.py)
Shows expected dashboard routing for all users:
```bash
python test_role_routing.py
```

### Manual Testing
1. Login as different users:
   - **hiring_manager** → Should see `/employer-dashboard/` with hiring manager nav
   - **rpo_admin** → Should see `/employer-dashboard/` with rpo admin nav
   - **candidate** → Should see `/candidate-dashboard/` with candidate nav

2. Verify navigation menus:
   - Each role should see only their specific navigation items
   - Dropdowns should show appropriate actions for that role
   - URLs should all work correctly

## Creating New User Roles

### Step 1: Create Django Group
```python
from django.contrib.auth.models import Group
group, created = Group.objects.get_or_create(name='new_role_name')
```

### Step 2: Create User with Role
```python
from django.contrib.auth.models import User
from App.models import Profile

user = User.objects.create_user(username='username', password='password')
profile = Profile.objects.create(user=user, role='new_role_name')
user.groups.add(group)
```

### Step 3: Create Navigation Group
```python
from App.models import NavigationGroup

nav_group = NavigationGroup.objects.create(
    name='New Role Menu',
    visible_to_roles=['new_role_name'],
    icon='fa fa-briefcase',
    order=1,
    is_active=True
)
```

### Step 4: Create Navigation Items
```python
from App.models import NavigationItem

NavigationItem.objects.create(
    group=nav_group,
    name='Menu Item',
    url='/url-path/',
    icon='fa fa-icon',
    order=1,
    is_active=True
)
```

### Step 5: Update auth_views.py
Add routing logic for the new role in the login_view function.

## API Endpoints

### Get Navigation for Current User
```
GET /api/navigation/user/
Response: {
    "success": true,
    "data": {
        "groups": [
            {
                "id": 1,
                "name": "Job Management",
                "icon": "fa fa-briefcase",
                "items": [...]
            }
        ]
    }
}
```

### Get All Navigation Groups
```
GET /api/navigation/groups/
```

### Get Navigation Items by Group
```
GET /api/navigation/groups/<group_id>/items/
```

## Benefits of This System

1. **Dynamic**: Navigation is database-driven, can be updated without code changes
2. **Role-Based**: Each user sees only relevant navigation items
3. **Maintainable**: Centralized navigation logic in service layer
4. **Extensible**: Easy to add new roles and navigation items
5. **Consistent**: Same MVT pattern across all dashboards
6. **Secure**: Role-based access control at login level

## Troubleshooting

### User sees wrong dashboard
1. Check `user.profile.role` field: `python manage.py shell` → `User.objects.get(username='name').profile.role`
2. Check user's groups: `User.objects.get(username='name').groups.all()`
3. Run: `python fix_all_user_roles.py` to reset roles

### Navigation not showing
1. Check if NavigationGroup has correct `visible_to_roles`
2. Verify NavigationGroup `is_active=True`
3. Check if context processor is enabled in settings.py
4. Verify user has correct role in database

### New role not routing correctly
1. Add role to auth_views.py login routing logic
2. Create corresponding NavigationGroup with role in `visible_to_roles`
3. Update fix_all_user_roles.py if needed for bulk user updates

## Files Modified

1. **App/views/auth_views.py**: Role-based login routing
2. **App/services/navigation_service.py**: Navigation business logic
3. **App/context_processors_navigation.py**: Auto-inject navigation
4. **templates/Components/For-Employer/dashboard_nav.html**: MVT navigation template
5. **templates/Components/For-Candidate/dashboard_nav.html**: MVT navigation template
6. **App/models.py**: NavigationGroup and NavigationItem models
7. **fix_all_user_roles.py**: Bulk user role update script
8. **test_role_routing.py**: Testing script for routing verification

## Next Steps

1. ✅ All users have correct roles assigned
2. ✅ Role-based dashboard routing implemented
3. ✅ Navigation templates converted to MVT pattern
4. Create candidate-specific navigation items in database (currently using fallback)
5. Test login flow with each user type
6. Add RPO-specific navigation items if needed
7. Document any custom dashboard widgets per role
