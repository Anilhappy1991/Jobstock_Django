# Reusable Navigation System - Complete Guide

## Overview
The reusable navigation system is a database-driven, role-based component system that provides dynamic navigation, dashboard widgets, and quick actions for all three user groups (Hiring Manager, Candidate, RPO Admin).

## Key Features

✅ **Database-Driven**: All navigation items, widgets, and actions stored in database  
✅ **Role-Based**: Content adapts automatically based on user role  
✅ **Reusable Components**: Single template works for all user groups  
✅ **Customizable**: Users can hide widgets and customize their dashboard  
✅ **Service Layer**: All business logic in NavigationService  
✅ **Context Processor**: Navigation data available in all templates globally

---

## Architecture

### 1. Models (`App/models/navigation.py`)

#### NavigationGroup
Groups related navigation items together (e.g., "Main Menu", "Settings")

```python
NavigationGroup(
    name='Main Menu',
    slug='main-menu',
    icon='fas fa-bars',
    visible_to_roles=['hiring_manager', 'candidate'],  # Who can see this group
    order=1
)
```

#### NavigationItem
Individual menu items with support for hierarchical navigation

```python
NavigationItem(
    group=main_menu_group,
    title='Dashboard',
    url_name='employer_dashboard',  # Django URL name
    icon='fas fa-home',
    visible_to_roles=['hiring_manager'],
    parent=None,  # Top-level item
    order=1,
    badge_text='3',  # Optional badge
    badge_class='badge-danger'
)
```

#### DashboardWidget
Dashboard cards/widgets for each role

```python
DashboardWidget(
    title='Active Jobs',
    widget_type='stat_card',  # stat_card, chart, table, list, activity, custom
    icon='fas fa-briefcase',
    data_source='/api/jobs/count/active/',  # API endpoint for data
    visible_to_roles=['hiring_manager'],
    grid_column='1',  # CSS grid column
    order=1
)
```

#### QuickAction
Quick action buttons for common tasks

```python
QuickAction(
    title='Post New Job',
    description='Create a new job posting',
    icon='fas fa-plus-circle',
    url_name='employer_submit_job',
    button_class='btn-primary',
    visible_to_roles=['hiring_manager'],
    order=1
)
```

#### UserDashboardPreference
Store user-specific customizations

```python
UserDashboardPreference(
    user=user,
    hidden_widgets=[1, 5, 7],  # Widget IDs to hide
    widget_order={'3': 1, '4': 2},  # Custom widget ordering
    theme='dark',  # User theme preference
    sidebar_collapsed=True
)
```

---

### 2. Service Layer (`App/services/navigation_service.py`)

#### NavigationService Methods

**get_navigation_for_user(user)**
```python
# Returns navigation menu structure for user's role
response = NavigationService.get_navigation_for_user(request.user)
# Response: {
#     'success': True,
#     'data': {
#         'navigation': [
#             {
#                 'id': 1,
#                 'name': 'Main Menu',
#                 'items': [
#                     {
#                         'title': 'Dashboard',
#                         'url': '/employer/dashboard/',
#                         'icon': 'fas fa-home',
#                         'children': []
#                     }
#                 ]
#             }
#         ]
#     }
# }
```

**get_dashboard_widgets(user)**
```python
# Returns widgets visible to user's role
response = NavigationService.get_dashboard_widgets(request.user)
# Response: {
#     'success': True,
#     'data': {
#         'widgets': [
#             {
#                 'id': 1,
#                 'title': 'Active Jobs',
#                 'type': 'stat_card',
#                 'data_source': '/api/jobs/count/active/',
#                 'order': 1
#             }
#         ]
#     }
# }
```

**get_quick_actions(user)**
```python
# Returns quick action buttons for user's role
response = NavigationService.get_quick_actions(request.user)
```

**get_complete_dashboard_data(user)**
```python
# Returns everything in one call (navigation + widgets + actions)
response = NavigationService.get_complete_dashboard_data(request.user)
# Used by context processor to provide all dashboard data globally
```

**update_user_preferences(user, preferences_data)**
```python
# Update user's dashboard preferences
response = NavigationService.update_user_preferences(request.user, {
    'hidden_widgets': [1, 5],
    'theme': 'dark',
    'sidebar_collapsed': True
})
```

---

### 3. Context Processor (`App/context_processors_navigation.py`)

Automatically injects `dashboard_data` into all template contexts:

```python
# In settings.py TEMPLATES context_processors:
"App.context_processors_navigation.navigation_context",

# Now available in ALL templates:
{{ dashboard_data.navigation }}
{{ dashboard_data.widgets }}
{{ dashboard_data.quick_actions }}
{{ dashboard_data.user }}
```

---

### 4. Reusable Template Components

#### Base Template (`templates/Base/dashboard_base.html`)
The unified base template for all dashboards:

```django
{% extends 'Base/dashboard_base.html' %}

{% block title %}My Custom Page{% endblock %}

{% block page_title %}My Custom Page{% endblock %}

{% block content %}
<!-- Your page content here -->
{% endblock %}
```

Features:
- Automatic sidebar navigation
- Top header with user info and notifications
- Breadcrumbs
- Quick actions section
- Dashboard widgets section
- Responsive layout

#### Navigation Component (`templates/Components/Common/navigation.html`)
```django
{% include 'Components/Common/navigation.html' with navigation=dashboard_data.navigation %}
```

Features:
- Hierarchical menu structure
- Active link highlighting
- Submenu support
- Badge support
- Icon support
- Mobile responsive

#### Dashboard Widgets Component (`templates/Components/Common/dashboard_widgets.html`)
```django
{% include 'Components/Common/dashboard_widgets.html' with widgets=dashboard_data.widgets %}
```

Widget Types:
- **stat_card**: Number/statistic cards
- **chart**: Chart visualizations (with Chart.js)
- **table**: Tabular data
- **list**: List items
- **activity**: Activity timeline
- **custom**: Custom HTML content

#### Quick Actions Component (`templates/Components/Common/quick_actions.html`)
```django
{% include 'Components/Common/quick_actions.html' with quick_actions=dashboard_data.quick_actions %}
```

Features:
- Grid layout of action buttons
- Icon and description support
- Color variations (btn-primary, btn-success, etc.)
- Responsive cards

---

## Setup Instructions

### Step 1: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Populate Initial Data

```bash
python manage.py populate_navigation
```

This creates:
- Navigation groups and items for all 3 user roles
- Dashboard widgets for all 3 user roles
- Quick actions for all 3 user roles

### Step 3: Verify Settings

Ensure `settings.py` includes the navigation context processor:

```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'App.context_processors_navigation.navigation_context',  # ← This line
            ],
        },
    },
]
```

---

## Usage Examples

### Example 1: Create a New Dashboard Page

```django
{# templates/pages/employer_custom_page.html #}
{% extends 'Base/dashboard_base.html' %}

{% block title %}Custom Page{% endblock %}

{% block page_title %}My Custom Dashboard{% endblock %}
{% block page_description %}
    <p class="page-description">This is my custom dashboard page</p>
{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-12">
        <div class="card">
            <div class="card-body">
                <h5>Custom Content</h5>
                <p>Your content here...</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**Result**: Page automatically includes:
- Sidebar navigation (role-specific)
- Top header with user info
- Breadcrumbs
- Quick actions (if defined in base template)
- Your custom content

---

### Example 2: Customize Quick Actions Section

```django
{% extends 'Base/dashboard_base.html' %}

{% block quick_actions %}
{# Override to show quick actions only on specific pages #}
{% if show_quick_actions %}
    {% include 'Components/Common/quick_actions.html' with quick_actions=dashboard_data.quick_actions %}
{% endif %}
{% endblock %}
```

---

### Example 3: Add Custom Widgets

```django
{% extends 'Base/dashboard_base.html' %}

{% block dashboard_widgets %}
{# Show default widgets #}
{% include 'Components/Common/dashboard_widgets.html' with widgets=dashboard_data.widgets %}

{# Add custom widget #}
<div class="widget-card">
    <div class="widget-header">
        <h5>My Custom Widget</h5>
    </div>
    <div class="widget-body">
        <!-- Custom content -->
    </div>
</div>
{% endblock %}
```

---

### Example 4: Add Navigation Items Programmatically

```python
# In views.py or management command
from App.models.navigation import NavigationGroup, NavigationItem

# Get group
main_menu = NavigationGroup.objects.get(slug='hm-main')

# Add new navigation item
NavigationItem.objects.create(
    group=main_menu,
    title='New Feature',
    url_name='employer_new_feature',
    icon='fas fa-star',
    visible_to_roles=['hiring_manager'],
    order=10
)
```

---

### Example 5: Load Widget Data via AJAX

```javascript
// In your template
<script>
function loadWidgetData(widgetId, dataSource) {
    fetch(dataSource)
        .then(response => response.json())
        .then(data => {
            // Update widget with data
            const widget = document.querySelector(`[data-widget-id="${widgetId}"]`);
            const valueEl = widget.querySelector('[data-stat-value]');
            valueEl.textContent = data.count;
        });
}

// Load all widgets on page load
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-source]').forEach(widget => {
        const dataSource = widget.dataset.source;
        const widgetId = widget.closest('[data-widget-id]').dataset.widgetId;
        loadWidgetData(widgetId, dataSource);
    });
});
</script>
```

---

## Database Schema

```sql
-- Navigation Groups
CREATE TABLE navigation_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    slug VARCHAR(50) UNIQUE,
    icon VARCHAR(50),
    visible_to_roles JSON,
    order INTEGER,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Navigation Items
CREATE TABLE navigation_item (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES navigation_group(id),
    parent_id INTEGER REFERENCES navigation_item(id),
    title VARCHAR(100),
    url_name VARCHAR(100),
    icon VARCHAR(50),
    visible_to_roles JSON,
    requires_permission VARCHAR(100),
    badge_text VARCHAR(20),
    badge_class VARCHAR(50),
    order INTEGER,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Dashboard Widgets
CREATE TABLE dashboard_widget (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    widget_type VARCHAR(20),
    icon VARCHAR(50),
    description TEXT,
    data_source VARCHAR(255),
    visible_to_roles JSON,
    grid_column VARCHAR(50),
    order INTEGER,
    css_class VARCHAR(100),
    color_class VARCHAR(50),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Quick Actions
CREATE TABLE quick_action (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    icon VARCHAR(50),
    url_name VARCHAR(100),
    button_class VARCHAR(50),
    visible_to_roles JSON,
    order INTEGER,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- User Dashboard Preferences
CREATE TABLE user_dashboard_preference (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id),
    hidden_widgets JSON,
    widget_order JSON,
    theme VARCHAR(20),
    sidebar_collapsed BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

---

## Role Configuration

### Hiring Manager
- **Navigation**: Dashboard, Job Management, Applications, Candidates
- **Widgets**: Active Jobs, New Applications, Recent Applications
- **Quick Actions**: Post New Job, Review Applications, Search Candidates

### Candidate
- **Navigation**: Dashboard, Find Jobs, My Applications, Saved Jobs, My Profile
- **Widgets**: Jobs Applied, Profile Views, Recommended Jobs, Application Status
- **Quick Actions**: Find Jobs, Update Resume, Track Applications

### RPO Admin
- **Navigation**: Dashboard, Clients, All Jobs, Analytics, Reports
- **Widgets**: Total Clients, All Jobs, Placement Rate, Client Performance
- **Quick Actions**: Add Client, View Analytics, Generate Report

---

## Customization

### Add a New Widget Type

1. **Update Model** (already supports custom types via `widget_type` field)

2. **Add Template Logic** in `dashboard_widgets.html`:
```django
{% elif widget.type == 'my_custom_type' %}
<div class="my-custom-widget">
    <!-- Custom widget HTML -->
</div>
{% endif %}
```

3. **Create Widget**:
```python
DashboardWidget.objects.create(
    title='My Custom Widget',
    widget_type='my_custom_type',
    data_source='/api/my-data/',
    visible_to_roles=['hiring_manager'],
)
```

### Change Role Names

Update the `visible_to_roles` JSON field in database:
```python
# Update all hiring_manager to company_admin
for item in NavigationItem.objects.filter(visible_to_roles__contains=['hiring_manager']):
    roles = item.visible_to_roles
    roles = ['company_admin' if r == 'hiring_manager' else r for r in roles]
    item.visible_to_roles = roles
    item.save()
```

---

## API Integration

### Create Widget Data Endpoints

```python
# In views.py or api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from App.utils.response import DRFResponse

@api_view(['GET'])
def get_active_jobs_count(request):
    """API endpoint for Active Jobs widget"""
    count = Job.objects.filter(
        employer=request.user,
        status='active'
    ).count()
    
    return DRFResponse.success(data={
        'count': count,
        'label': 'Active Jobs'
    })

# In urls.py
urlpatterns = [
    path('api/jobs/count/active/', get_active_jobs_count, name='api_active_jobs_count'),
]
```

---

## Testing

### Test Navigation Service

```python
# In Django shell
from django.contrib.auth.models import User
from App.services import NavigationService

user = User.objects.get(username='hiring_manager')

# Get navigation
nav = NavigationService.get_navigation_for_user(user)
print(nav)

# Get widgets
widgets = NavigationService.get_dashboard_widgets(user)
print(widgets)

# Get all dashboard data
data = NavigationService.get_complete_dashboard_data(user)
print(data)
```

---

## Troubleshooting

### Navigation Not Showing
1. Check user has a role: `user.profile.role`
2. Verify navigation items exist: `NavigationItem.objects.all()`
3. Check `visible_to_roles` includes user's role
4. Ensure context processor is in settings.py

### Widgets Not Loading Data
1. Check `data_source` URL is correct
2. Verify API endpoint exists and works
3. Check browser console for JavaScript errors
4. Ensure CORS settings allow requests

### Context Processor Not Working
1. Verify in `settings.py` TEMPLATES context_processors
2. Restart Django server after adding context processor
3. Check user is authenticated: `{% if request.user.is_authenticated %}`

---

## Performance Optimization

### Reduce Database Queries

```python
# In NavigationService
nav_groups = NavigationGroup.objects.filter(
    is_active=True
).prefetch_related(
    'items',
    'items__children'
)  # Reduces N+1 queries
```

### Cache Navigation Data

```python
from django.core.cache import cache

def get_navigation_for_user(cls, user):
    cache_key = f'navigation_{user.id}_{user.profile.role}'
    cached = cache.get(cache_key)
    
    if cached:
        return cached
    
    # ... build navigation ...
    
    cache.set(cache_key, result, 3600)  # Cache for 1 hour
    return result
```

---

## Best Practices

1. **Always use URL names**, never hardcode URLs
2. **Use role-based visibility** instead of permission checks when possible
3. **Keep widget data sources lightweight** - return only necessary data
4. **Cache navigation data** for better performance
5. **Use semantic icons** from Font Awesome
6. **Test with all three user roles** before deploying
7. **Document custom widgets** for other developers

---

## Summary

This reusable navigation system provides:

✅ **Single codebase** serves all 3 user groups  
✅ **Database-driven** - no code changes for content updates  
✅ **Role-based** - automatic filtering by user role  
✅ **Customizable** - users can personalize their dashboard  
✅ **Service layer** - clean separation of concerns  
✅ **REST API ready** - widgets can fetch data from APIs  

**Start using it**: Just extend `dashboard_base.html` and your page gets navigation, widgets, and quick actions automatically!
