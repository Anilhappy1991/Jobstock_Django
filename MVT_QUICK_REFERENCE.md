# MVT Navigation - Quick Reference Card

## 🚀 Quick Start

### Using Navigation in Views
```python
from App.services.navigation_service import NavigationService

# Automatic (via context processor)
def my_view(request):
    # navigation_groups is automatically available
    return render(request, 'template.html')

# Manual (if needed)
def my_view(request):
    service = NavigationService()
    nav_response = service.get_navigation_for_user(request.user)
    
    if nav_response.get('success'):
        navigation = nav_response['data']['navigation']
    
    return render(request, 'template.html', {'nav': navigation})
```

### Using Navigation in Templates
```django
{# Server-side rendering #}
{% for group in navigation_groups %}
    <h4>{{ group.name }}</h4>
    {% for item in group.items %}
        <a href="{{ item.url }}">
            <i class="{{ item.icon }}"></i>{{ item.title }}
        </a>
    {% endfor %}
{% endfor %}
```

### Using REST API in JavaScript
```javascript
// Fetch navigation
async function loadNav() {
    const response = await fetch('/api/navigation/');
    const data = await response.json();
    if (data.success) {
        console.log(data.data.navigation);
    }
}

// Get stats
async function loadStats() {
    const response = await fetch('/api/navigation/stats/');
    const data = await response.json();
    if (data.success) {
        console.log(data.data);
    }
}
```

## 📋 Available API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/navigation/` | GET | Get user's navigation |
| `/api/navigation/stats/` | GET | Get badge statistics |
| `/api/dashboard/widgets/` | GET | Get dashboard widgets |
| `/api/dashboard/quick-actions/` | GET | Get quick actions |
| `/api/navigation/json/` | GET | Export navigation as JSON |
| `/api/dashboard/preferences/` | POST | Update preferences |

## 🎯 Response Format

All API responses use `ApiResponse` class:

```json
{
  "success": true,
  "status_code": 200,
  "message": "Operation successful",
  "data": { ... }
}
```

## 🔧 Creating API Responses

```python
from App.utils.response import ApiResponse

# Success
return ApiResponse.success(
    data={'key': 'value'},
    message="Success message"
)

# Error
return ApiResponse.error(
    message="Error message",
    error_details={'field': 'error'}
)

# Other methods
ApiResponse.created(...)      # 201
ApiResponse.not_found(...)    # 404
ApiResponse.unauthorized(...) # 401
ApiResponse.forbidden(...)    # 403
ApiResponse.validation_error(...) # 422
ApiResponse.server_error(...) # 500
```

## 🗄️ Service Layer Methods

```python
from App.services.navigation_service import NavigationService

service = NavigationService()

# Get navigation
nav_response = service.get_navigation_for_user(user)

# Get widgets
widgets_response = service.get_dashboard_widgets(user)

# Get quick actions
actions_response = service.get_quick_actions(user)

# Get statistics
stats_response = service.get_navigation_stats(user)
```

## 🎨 Template Context Variables

Available in ALL templates via context processor:

```django
{{ navigation_groups }}    {# List of navigation groups #}
{{ dashboard_widgets }}    {# List of dashboard widgets #}
{{ quick_actions }}        {# List of quick actions #}
{{ navigation_stats }}     {# Dictionary of statistics #}
```

## 🔐 Role-Based Access

Navigation automatically filters by user role:
- `hiring_manager` - Can post jobs, view applicants
- `candidate` - Can apply for jobs
- `rpo_admin` - Admin features
- `all` - Visible to everyone

## 🏷️ Badge Classes

```html
<span class="badge badge-primary">Blue</span>
<span class="badge badge-danger">Red/Alert</span>
<span class="badge badge-success">Green</span>
<span class="badge badge-warning">Yellow</span>
<span class="badge badge-info">Cyan</span>
```

## 🧪 Testing

```bash
# Verify implementation
python verify_mvt_navigation.py

# Populate navigation data
python manage.py setup_hiring_manager_navigation

# Start server
python manage.py runserver
```

## 📂 Key Files

| File | Purpose |
|------|---------|
| `App/models.py` | NavigationGroup, NavigationItem models |
| `App/services/navigation_service.py` | Service layer logic |
| `App/views/api_navigation_views.py` | REST API endpoints |
| `App/utils/response.py` | ApiResponse class |
| `App/context_processors_navigation.py` | Context processor |
| `templates/Components/For-Employer/dashboard_nav.html` | Server-side template |
| `templates/Components/For-Employer/dashboard_nav_api.html` | AJAX template |

## 🐛 Troubleshooting

**Navigation not showing?**
- Check context processor is enabled in `settings.py`
- Verify user is authenticated
- Check user has correct role assigned

**API returns 401?**
- Ensure `@login_required` decorator on API views
- User must be logged in

**Badges not updating?**
- Check `get_navigation_stats()` returns correct data
- Verify JavaScript refresh interval

**URL not found warnings?**
- Create missing URL patterns in `urls.py`
- Use `url` field instead of `url_name` if direct URL needed

## 📝 Common Patterns

### Add New Navigation Item (via admin/code)
```python
from App.models import NavigationGroup, NavigationItem

group = NavigationGroup.objects.get(slug='main-menu')

NavigationItem.objects.create(
    group=group,
    title='New Feature',
    url_name='new_feature_url',
    icon='fa-solid fa-star',
    visible_to_roles=['hiring_manager'],
    order=10
)
```

### Create Child Menu Item
```python
parent = NavigationItem.objects.get(title='Reports')

NavigationItem.objects.create(
    group=parent.group,
    parent=parent,
    title='Monthly Report',
    url_name='monthly_report',
    icon='fa-solid fa-file',
    visible_to_roles=['hiring_manager'],
    order=1
)
```

### Update Badge Dynamically
```python
# In view or context processor
def update_badges(request):
    unread_count = Message.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    
    item = NavigationItem.objects.get(url_name='messages')
    item.badge_text = str(unread_count)
    item.badge_class = 'badge-danger' if unread_count > 0 else 'badge-secondary'
    item.save()
```

## ✅ Verification Checklist

- [ ] `python verify_mvt_navigation.py` passes all 5 tests
- [ ] Navigation displays in browser
- [ ] API endpoints return correct JSON
- [ ] Badges show correct counts
- [ ] Role-based filtering works
- [ ] Hierarchical menus expand/collapse
- [ ] Active state highlights current page

---

**Need more details?** See `MVT_NAVIGATION_IMPLEMENTATION.md`

**Status:** ✅ COMPLETE | **Version:** 1.0.0 | **Date:** Dec 21, 2025
