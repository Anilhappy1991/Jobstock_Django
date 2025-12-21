# Reusable Navigation System - Quick Reference

## 🚀 Quick Start

### 1. Run Migrations & Populate Data
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py populate_navigation
```

### 2. Create a Dashboard Page
```django
{# templates/pages/my_dashboard.html #}
{% extends 'Base/dashboard_base.html' %}

{% block title %}My Page{% endblock %}
{% block page_title %}My Dashboard{% endblock %}

{% block content %}
    <!-- Your content here -->
{% endblock %}
```

**Done!** Your page now has:
- ✅ Role-specific sidebar navigation
- ✅ Top header with user info
- ✅ Quick actions
- ✅ Dashboard widgets

---

## 📦 Components

### Include Navigation
```django
{% include 'Components/Common/navigation.html' with navigation=dashboard_data.navigation %}
```

### Include Widgets
```django
{% include 'Components/Common/dashboard_widgets.html' with widgets=dashboard_data.widgets %}
```

### Include Quick Actions
```django
{% include 'Components/Common/quick_actions.html' with quick_actions=dashboard_data.quick_actions %}
```

---

## 🎯 Service Layer Methods

```python
from App.services import NavigationService

# Get navigation for user
NavigationService.get_navigation_for_user(user)

# Get dashboard widgets
NavigationService.get_dashboard_widgets(user)

# Get quick actions
NavigationService.get_quick_actions(user)

# Get everything at once
NavigationService.get_complete_dashboard_data(user)

# Update user preferences
NavigationService.update_user_preferences(user, {
    'hidden_widgets': [1, 5],
    'theme': 'dark'
})
```

---

## 🔧 Add Navigation Item

```python
from App.models.navigation import NavigationGroup, NavigationItem

# Get group
group = NavigationGroup.objects.get(slug='hm-main')

# Create item
NavigationItem.objects.create(
    group=group,
    title='New Feature',
    url_name='my_view_name',  # Django URL name
    icon='fas fa-star',
    visible_to_roles=['hiring_manager'],
    order=10
)
```

---

## 📊 Add Dashboard Widget

```python
from App.models.navigation import DashboardWidget

DashboardWidget.objects.create(
    title='My Stats',
    widget_type='stat_card',  # stat_card, chart, table, list
    icon='fas fa-chart-bar',
    description='My statistics',
    data_source='/api/my-stats/',  # API endpoint
    visible_to_roles=['hiring_manager'],
    grid_column='1',
    order=5,
    color_class='bg-primary'
)
```

---

## ⚡ Add Quick Action

```python
from App.models.navigation import QuickAction

QuickAction.objects.create(
    title='Do Something',
    description='Quick action description',
    icon='fas fa-bolt',
    url_name='my_action_view',
    button_class='btn-primary',
    visible_to_roles=['hiring_manager'],
    order=5
)
```

---

## 👥 User Roles

Available roles:
- `hiring_manager` - Hiring Manager/Employer
- `candidate` - Job Seeker/Candidate
- `rpo_admin` - RPO Administrator
- `all` - Show to all roles

---

## 🎨 Widget Types

| Type | Description | Use For |
|------|-------------|---------|
| `stat_card` | Number/statistic | Counts, totals |
| `chart` | Chart visualization | Graphs, charts |
| `table` | Tabular data | Lists with columns |
| `list` | Simple list | Recent items |
| `activity` | Timeline | Activity feed |
| `custom` | Custom HTML | Anything else |

---

## 🔍 Template Variables

Available globally via context processor:

```django
{{ dashboard_data.navigation }}      {# Navigation items #}
{{ dashboard_data.widgets }}          {# Dashboard widgets #}
{{ dashboard_data.quick_actions }}    {# Quick action buttons #}
{{ dashboard_data.user.username }}    {# User info #}
{{ dashboard_data.user.role }}        {# User role #}
{{ dashboard_data.user.full_name }}   {# Full name #}
```

---

## 🎯 Template Blocks

Override these in your templates:

```django
{% block title %}{% endblock %}              {# Page title #}
{% block page_title %}{% endblock %}          {# H1 heading #}
{% block page_description %}{% endblock %}    {# Subtitle #}
{% block breadcrumb %}{% endblock %}          {# Breadcrumbs #}
{% block quick_actions %}{% endblock %}       {# Quick actions section #}
{% block dashboard_widgets %}{% endblock %}   {# Widgets section #}
{% block content %}{% endblock %}             {# Main content #}
{% block extra_css %}{% endblock %}           {# Additional CSS #}
{% block extra_js %}{% endblock %}            {# Additional JS #}
```

---

## 📡 Create Widget Data API

```python
from rest_framework.decorators import api_view
from App.utils.response import DRFResponse

@api_view(['GET'])
def my_widget_data(request):
    return DRFResponse.success(data={
        'count': 42,
        'label': 'Total Items'
    })

# Add to urls.py
path('api/my-widget/', my_widget_data, name='api_my_widget'),
```

---

## 🔒 Role-Based Access

```python
# In model
visible_to_roles = ['hiring_manager', 'candidate']

# In template
{% if user.profile.role == 'hiring_manager' %}
    <!-- Hiring Manager only content -->
{% endif %}

# In view
if request.user.profile.role != 'hiring_manager':
    return redirect('home')
```

---

## 🛠️ Customization Examples

### Hide Quick Actions on Specific Page
```django
{% extends 'Base/dashboard_base.html' %}

{% block quick_actions %}
    {# Don't show quick actions on this page #}
{% endblock %}
```

### Add Custom Widget
```django
{% block dashboard_widgets %}
    {# Include default widgets #}
    {{ block.super }}
    
    {# Add custom widget #}
    <div class="widget-card">
        <h5>My Custom Widget</h5>
    </div>
{% endblock %}
```

### Custom Breadcrumb
```django
{% block breadcrumb %}
<nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Home</a></li>
        <li class="breadcrumb-item"><a href="{% url 'jobs' %}">Jobs</a></li>
        <li class="breadcrumb-item active">Details</li>
    </ol>
</nav>
{% endblock %}
```

---

## 🧪 Testing

```python
# Django shell
python manage.py shell

from django.contrib.auth.models import User
from App.services import NavigationService

# Get user
user = User.objects.get(username='hiring_manager')

# Test navigation
nav = NavigationService.get_navigation_for_user(user)
print(nav['data']['navigation'])

# Test widgets
widgets = NavigationService.get_dashboard_widgets(user)
print(widgets['data']['widgets'])
```

---

## 📋 Common Tasks

### Update Navigation Order
```python
item = NavigationItem.objects.get(title='Dashboard')
item.order = 1
item.save()
```

### Hide Navigation Item
```python
item = NavigationItem.objects.get(title='Reports')
item.is_active = False
item.save()
```

### Change Widget Visibility
```python
widget = DashboardWidget.objects.get(title='Active Jobs')
widget.visible_to_roles = ['hiring_manager', 'rpo_admin']
widget.save()
```

### Add Badge to Menu Item
```python
item = NavigationItem.objects.get(title='Applications')
item.badge_text = '5'
item.badge_class = 'badge-danger'
item.save()
```

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| Navigation not showing | Check user has role: `user.profile.role` |
| Widget not loading | Verify `data_source` URL exists |
| Permission denied | Check `visible_to_roles` includes user's role |
| Template not found | Ensure `TEMPLATES` dirs includes templates folder |
| Context data missing | Verify context processor in settings.py |

---

## 📚 Files Reference

```
App/
  models/
    navigation.py              # Navigation models
  services/
    navigation_service.py      # Navigation service
  context_processors_navigation.py  # Context processor
  management/commands/
    populate_navigation.py     # Seed data command

templates/
  Base/
    dashboard_base.html        # Base dashboard template
  Components/Common/
    navigation.html            # Navigation component
    dashboard_widgets.html     # Widgets component
    quick_actions.html         # Quick actions component

docs/
  REUSABLE_NAVIGATION_SYSTEM.md  # Full documentation
```

---

## 💡 Tips

1. ✅ Always use Django URL names, never hardcoded URLs
2. ✅ Test with all 3 user roles before deploying
3. ✅ Cache navigation data for performance
4. ✅ Use semantic icons from Font Awesome
5. ✅ Keep widget APIs fast and lightweight
6. ✅ Document custom widgets for team
7. ✅ Use `prefetch_related()` to reduce queries

---

## 🎉 That's It!

The system automatically:
- Shows correct navigation based on user role
- Loads appropriate widgets for each role
- Displays relevant quick actions
- Handles user preferences

Just extend `dashboard_base.html` and you're done! 🚀
