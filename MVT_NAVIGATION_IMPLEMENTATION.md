# MVT Navigation Implementation - Complete Guide

## Overview
This document explains the complete Model-View-Template (MVT) implementation for the navigation system with REST API support and reusable response classes.

## Architecture Components

### 1. Model Layer
**Files:**
- `App/models.py` - NavigationGroup, NavigationItem, DashboardWidget models

**Purpose:**
- Database structure for navigation system
- Stores menu items, groups, permissions, badges
- Supports role-based access control

**Key Models:**
```python
NavigationGroup:
    - name: Group name (e.g., "Main Menu")
    - order: Display order
    - roles: Allowed user roles
    - is_active: Visibility flag

NavigationItem:
    - title: Menu item title
    - url/url_name: Link destination
    - icon: Font Awesome icon class
    - group: Foreign key to NavigationGroup
    - parent: Self-referencing for hierarchical menus
    - badge_text/badge_class: Badge display
    - order: Display order within group
    - roles: Allowed user roles
```

### 2. Service Layer
**File:** `App/services/navigation_service.py`

**Purpose:**
- Business logic separation
- Database query optimization
- Reusable navigation methods
- Role-based filtering

**Key Methods:**
```python
NavigationService:
    - get_navigation_for_user(user) → List[Dict]
      Returns navigation structure for specific user role
      
    - get_dashboard_widgets(user) → List[Dict]
      Returns dashboard widgets based on role
      
    - get_quick_actions(user) → List[Dict]
      Returns quick action buttons for user
      
    - get_navigation_stats(user) → Dict
      Returns badge counts (notifications, messages, etc.)
```

**Usage Example:**
```python
from App.services.navigation_service import NavigationService

service = NavigationService()
navigation = service.get_navigation_for_user(request.user)
stats = service.get_navigation_stats(request.user)
```

### 3. View Layer

#### A. REST API Views
**File:** `App/views/api_navigation_views.py`

**Purpose:**
- AJAX endpoints for dynamic navigation
- JSON response formatting
- Authentication & permission checks

**Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/navigation/` | GET | Get user's navigation structure |
| `/api/navigation/stats/` | GET | Get badge counts/statistics |
| `/api/dashboard/widgets/` | GET | Get dashboard widgets |
| `/api/dashboard/quick-actions/` | GET | Get quick action buttons |
| `/api/navigation/json/` | GET | Export navigation as JSON |
| `/api/dashboard/preferences/` | POST | Update user preferences |

**Example API Response:**
```json
{
    "success": true,
    "status_code": 200,
    "message": "Navigation retrieved successfully",
    "data": {
        "groups": [
            {
                "id": 1,
                "name": "Main Menu",
                "items": [
                    {
                        "id": 1,
                        "title": "Dashboard",
                        "url": "/employer/dashboard/",
                        "icon": "fa-solid fa-gauge-high",
                        "badge_text": "5",
                        "badge_class": "badge-danger"
                    }
                ]
            }
        ]
    }
}
```

#### B. Traditional Django Views
**File:** `App/views/employer_views.py`

**Purpose:**
- Server-side rendering
- Context data preparation
- Form handling

**Implementation:**
```python
from App.services.navigation_service import NavigationService

def employer_dashboard(request):
    service = NavigationService()
    
    context = {
        'navigation_groups': service.get_navigation_for_user(request.user),
        'dashboard_widgets': service.get_dashboard_widgets(request.user),
        'navigation_stats': service.get_navigation_stats(request.user),
    }
    
    return render(request, 'employer_dashboard.html', context)
```

### 4. Template Layer

#### A. Server-Side Rendering Template
**File:** `templates/Components/For-Employer/dashboard_nav.html`

**Purpose:**
- Traditional Django template rendering
- Server-generated HTML
- Uses context processor for data

**Key Features:**
- Dynamic menu generation from database
- Role-based visibility
- Hierarchical menu support (parent/child)
- Badge display
- Active state highlighting
- Fallback to static menu if data unavailable

**Template Code Example:**
```django
{% for group in navigation_groups %}
<ul data-submenu-title="{{ group.name }}">
    {% for item in group.items %}
        <li class="{% if dashboard_active == item.url_name %}active{% endif %}">
            <a href="{{ item.url }}">
                <i class="{{ item.icon }}"></i>{{ item.title }}
                {% if item.badge_text %}
                    <span class="badge {{ item.badge_class }}">{{ item.badge_text }}</span>
                {% endif %}
            </a>
        </li>
    {% endfor %}
</ul>
{% endfor %}
```

#### B. AJAX/REST API Template
**File:** `templates/Components/For-Employer/dashboard_nav_api.html`

**Purpose:**
- Client-side dynamic navigation
- AJAX loading via Fetch API
- Real-time badge updates

**Key Features:**
- Loading states
- Error handling
- Auto-refresh every 30 seconds
- XSS protection
- Async data loading

**JavaScript Example:**
```javascript
async function loadNavigation() {
    try {
        const response = await fetch('/api/navigation/');
        const result = await response.json();
        
        if (result.success) {
            renderNavigation(result.data);
        }
    } catch (error) {
        console.error('Error loading navigation:', error);
    }
}
```

### 5. Reusable Response Class
**File:** `App/utils/response.py`

**Purpose:**
- Standardized API response format
- Consistent error handling
- HTTP status code management

**Class Structure:**
```python
class ApiResponse:
    @staticmethod
    def success(data=None, message="Success", status_code=200):
        return JsonResponse({
            'success': True,
            'status_code': status_code,
            'message': message,
            'data': data
        }, status=status_code)
    
    @staticmethod
    def error(message, error_details=None, status_code=400):
        return JsonResponse({
            'success': False,
            'status_code': status_code,
            'message': message,
            'error': error_details
        }, status=status_code)
```

**Available Methods:**
- `success()` - 200 OK
- `created()` - 201 Created
- `error()` - 400 Bad Request
- `not_found()` - 404 Not Found
- `unauthorized()` - 401 Unauthorized
- `forbidden()` - 403 Forbidden
- `validation_error()` - 422 Unprocessable Entity
- `server_error()` - 500 Internal Server Error

**Usage Example:**
```python
from App.utils.response import ApiResponse

# Success response
return ApiResponse.success(
    data={'navigation': navigation_data},
    message="Navigation loaded successfully"
)

# Error response
return ApiResponse.error(
    message="Invalid user role",
    error_details={'role': 'Role not found'},
    status_code=400
)
```

### 6. Context Processor
**File:** `App/context_processors_navigation.py`

**Purpose:**
- Make navigation data available in ALL templates
- Automatic data loading
- No manual passing of context

**Configuration in settings.py:**
```python
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
            'App.context_processors_navigation.navigation_context',
        ],
    },
}]
```

**Available Template Variables:**
- `{{ navigation_groups }}` - All navigation groups and items
- `{{ dashboard_widgets }}` - Dashboard widget data
- `{{ quick_actions }}` - Quick action buttons
- `{{ navigation_stats }}` - Badge counts and statistics

## Data Flow Diagrams

### Server-Side Rendering Flow:
```
User Request
    ↓
Django View
    ↓
NavigationService (fetch from DB)
    ↓
Context Data
    ↓
Template Rendering
    ↓
HTML Response
```

### REST API Flow:
```
JavaScript Fetch
    ↓
API Endpoint
    ↓
NavigationService (fetch from DB)
    ↓
ApiResponse (standardized format)
    ↓
JSON Response
    ↓
JavaScript Rendering
```

## Setup Instructions

### 1. Run Migration (if not done)
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Populate Navigation Data
```bash
python manage.py setup_hiring_manager_navigation
```

### 3. Enable Context Processor
Add to `settings.py`:
```python
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            'App.context_processors_navigation.navigation_context',
        ],
    },
}]
```

### 4. Include API URLs
In `App/urls.py`:
```python
from django.urls import path, include

urlpatterns = [
    path("api/", include('App.urls_api_navigation')),
    # ... other urls
]
```

## Usage Examples

### Example 1: Server-Side Rendering in View
```python
from django.shortcuts import render
from App.services.navigation_service import NavigationService

def my_dashboard_view(request):
    # Context processor automatically adds navigation_groups
    # But you can also fetch manually if needed:
    service = NavigationService()
    
    context = {
        'dashboard_active': 'dashboard',
        # navigation_groups available from context processor
    }
    
    return render(request, 'dashboard.html', context)
```

### Example 2: AJAX Loading in Template
```html
<div id="navigation-container">
    <div class="loading">Loading navigation...</div>
</div>

<script>
async function loadNav() {
    const response = await fetch('/api/navigation/');
    const data = await response.json();
    
    if (data.success) {
        renderNavigation(data.data.groups);
    }
}

loadNav();
</script>
```

### Example 3: Custom API Endpoint
```python
from django.contrib.auth.decorators import login_required
from App.services.navigation_service import NavigationService
from App.utils.response import ApiResponse

@login_required
def my_custom_navigation_api(request):
    try:
        service = NavigationService()
        navigation = service.get_navigation_for_user(request.user)
        
        return ApiResponse.success(
            data={'navigation': navigation},
            message="Navigation retrieved"
        )
    except Exception as e:
        return ApiResponse.server_error(
            message="Failed to load navigation",
            error_details=str(e)
        )
```

## Database Schema

### NavigationGroup Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | CharField(100) | Group name |
| order | Integer | Display order |
| roles | JSONField | Allowed roles |
| is_active | Boolean | Visibility |

### NavigationItem Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| title | CharField(100) | Menu title |
| url | CharField(255) | Direct URL |
| url_name | CharField(100) | Django URL name |
| icon | CharField(100) | CSS class |
| group | ForeignKey | Navigation group |
| parent | ForeignKey(self) | Parent item |
| badge_text | CharField(20) | Badge content |
| badge_class | CharField(50) | Badge CSS |
| order | Integer | Display order |
| roles | JSONField | Allowed roles |
| is_active | Boolean | Visibility |

## Role-Based Navigation

### Supported Roles:
- `hiring_manager` - Can post jobs, view applicants
- `candidate` - Can apply for jobs, manage applications
- `admin` - Full access to all features

### Role Check in Service:
```python
def get_navigation_for_user(self, user):
    user_role = self.get_user_role(user)
    
    # Fetch groups where user's role is in allowed roles
    groups = NavigationGroup.objects.filter(
        is_active=True,
        roles__contains=user_role
    ).prefetch_related('items')
    
    return self._format_navigation_data(groups, user_role)
```

## Badge System

### Static Badges (from database):
```python
NavigationItem.objects.create(
    title="Messages",
    badge_text="New",
    badge_class="badge-danger"
)
```

### Dynamic Badges (from stats):
```python
def get_navigation_stats(self, user):
    if role == 'hiring_manager':
        return {
            'new_applications': JobApplication.objects.filter(
                job__employer=user,
                is_read=False
            ).count(),
            'unread_messages': Message.objects.filter(
                recipient=user,
                is_read=False
            ).count()
        }
```

## Testing

### Test Navigation Service:
```python
from django.test import TestCase
from App.services.navigation_service import NavigationService
from App.models import User

class NavigationServiceTest(TestCase):
    def test_get_navigation_for_hiring_manager(self):
        user = User.objects.create(username='test', role='hiring_manager')
        service = NavigationService()
        navigation = service.get_navigation_for_user(user)
        
        self.assertIsInstance(navigation, list)
        self.assertGreater(len(navigation), 0)
```

### Test API Endpoint:
```python
from django.test import Client

def test_navigation_api():
    client = Client()
    client.login(username='test', password='password')
    
    response = client.get('/api/navigation/')
    data = response.json()
    
    assert data['success'] == True
    assert 'groups' in data['data']
```

## Performance Optimization

### 1. Use Prefetch Related:
```python
groups = NavigationGroup.objects.prefetch_related(
    'items',
    'items__children'
).filter(is_active=True)
```

### 2. Cache Navigation:
```python
from django.core.cache import cache

def get_cached_navigation(user):
    cache_key = f'navigation_{user.role}_{user.id}'
    navigation = cache.get(cache_key)
    
    if not navigation:
        service = NavigationService()
        navigation = service.get_navigation_for_user(user)
        cache.set(cache_key, navigation, 300)  # 5 minutes
    
    return navigation
```

### 3. Database Indexing:
```python
class NavigationItem(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['group', 'order']),
            models.Index(fields=['parent', 'is_active']),
        ]
```

## Troubleshooting

### Issue: Navigation not showing
**Solution:** Check context processor is enabled in settings.py

### Issue: API returns 401 Unauthorized
**Solution:** Ensure user is logged in, add `@login_required` decorator

### Issue: Badges not updating
**Solution:** Check `get_navigation_stats()` method returns correct data

### Issue: Hierarchical menus not working
**Solution:** Verify parent-child relationships in database

## Summary

This MVT implementation provides:
✅ **Model Layer** - Database structure with NavigationGroup/NavigationItem
✅ **Service Layer** - NavigationService for business logic
✅ **View Layer** - Both REST API and traditional Django views
✅ **Template Layer** - Server-side and AJAX-based rendering
✅ **Reusable Response** - ApiResponse class for standardized responses
✅ **Context Processor** - Automatic navigation data in all templates
✅ **Role-Based Access** - Dynamic menus based on user role
✅ **Badge System** - Real-time counts and notifications

**Files Created/Modified:**
1. `App/models.py` - NavigationGroup, NavigationItem models
2. `App/services/navigation_service.py` - NavigationService class
3. `App/views/api_navigation_views.py` - REST API endpoints
4. `App/urls_api_navigation.py` - API URL configuration
5. `App/utils/response.py` - ApiResponse class
6. `templates/Components/For-Employer/dashboard_nav.html` - Server-side template
7. `templates/Components/For-Employer/dashboard_nav_api.html` - AJAX template
8. `App/context_processors_navigation.py` - Context processor
9. `App/management/commands/setup_hiring_manager_navigation.py` - Data setup

**Complete MVT Pattern Achieved!** 🎉
