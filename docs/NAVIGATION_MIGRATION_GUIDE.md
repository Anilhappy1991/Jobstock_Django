# Migration Guide: Using Reusable Navigation System

## Overview
This guide helps you migrate existing dashboard views to use the new reusable navigation system.

---

## Before Migration

### Old Approach (Without Reusable System)
Each view had its own navigation HTML, duplicated across multiple templates:

```django
{# OLD: templates/pages/employer_dashboard.html #}
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
</head>
<body>
    <!-- Hardcoded navigation -->
    <div class="sidebar">
        <a href="/employer/dashboard/">Dashboard</a>
        <a href="/employer/jobs/">Jobs</a>
        <a href="/employer/applications/">Applications</a>
    </div>
    
    <div class="main-content">
        <!-- Dashboard content -->
    </div>
</body>
</html>
```

**Problems:**
- ❌ Navigation duplicated in every template
- ❌ Must update multiple files to add/remove items
- ❌ No role-based filtering
- ❌ Hardcoded URLs break when routes change
- ❌ No database-driven configuration

---

## After Migration

### New Approach (With Reusable System)
Single base template, database-driven navigation:

```django
{# NEW: templates/pages/employer_dashboard.html #}
{% extends 'Base/dashboard_base.html' %}

{% block title %}Dashboard{% endblock %}
{% block page_title %}Dashboard{% endblock %}

{% block content %}
    <!-- Dashboard content only -->
{% endblock %}
```

**Benefits:**
- ✅ Navigation defined once in database
- ✅ Automatic role-based filtering
- ✅ Uses Django URL names (never break)
- ✅ Update navigation without touching code
- ✅ Reusable across all user groups

---

## Step-by-Step Migration

### Step 1: Setup (One Time)

```bash
# 1. Run migrations
python manage.py makemigrations
python manage.py migrate

# 2. Populate navigation data
python manage.py populate_navigation

# 3. Restart server
python manage.py runserver
```

### Step 2: Migrate Each Template

#### Example 1: Employer Dashboard

**OLD CODE:**
```django
{# templates/pages/employer_dashboard.html #}
{% extends 'Base/base.html' %}
{% load static %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <!-- Sidebar Navigation -->
        <div class="col-md-2 sidebar">
            <div class="nav-menu">
                <a href="{% url 'employer_dashboard' %}" class="nav-item active">
                    <i class="fas fa-home"></i> Dashboard
                </a>
                <a href="{% url 'employer_submit_job' %}" class="nav-item">
                    <i class="fas fa-plus"></i> Post Job
                </a>
                <a href="{% url 'employer_manage_jobs' %}" class="nav-item">
                    <i class="fas fa-briefcase"></i> Manage Jobs
                </a>
                <a href="{% url 'employer_applications' %}" class="nav-item">
                    <i class="fas fa-users"></i> Applications
                    <span class="badge badge-danger">3</span>
                </a>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="col-md-10">
            <div class="dashboard-header">
                <h1>Employer Dashboard</h1>
            </div>
            
            <!-- Stats Cards -->
            <div class="row">
                <div class="col-md-3">
                    <div class="stat-card">
                        <h3>{{ active_jobs_count }}</h3>
                        <p>Active Jobs</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <h3>{{ total_applications }}</h3>
                        <p>Applications</p>
                    </div>
                </div>
            </div>
            
            <!-- Recent Applications Table -->
            <div class="card mt-4">
                <div class="card-header">
                    <h5>Recent Applications</h5>
                </div>
                <div class="card-body">
                    <table class="table">
                        {% for app in applications %}
                        <tr>
                            <td>{{ app.candidate }}</td>
                            <td>{{ app.job_title }}</td>
                            <td>{{ app.status }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**NEW CODE:**
```django
{# templates/pages/employer_dashboard.html #}
{% extends 'Base/dashboard_base.html' %}

{% block title %}Employer Dashboard - Jobstock{% endblock %}

{% block page_title %}Employer Dashboard{% endblock %}
{% block page_description %}
    <p class="page-description">Welcome back! Here's your recruitment overview.</p>
{% endblock %}

{% block content %}
    <!-- Stats are now handled by widgets automatically -->
    
    <!-- Recent Applications Table -->
    <div class="card mt-4">
        <div class="card-header">
            <h5>Recent Applications</h5>
        </div>
        <div class="card-body">
            <table class="table">
                <thead>
                    <tr>
                        <th>Candidate</th>
                        <th>Job Title</th>
                        <th>Status</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {% for app in applications %}
                    <tr>
                        <td>{{ app.candidate.full_name }}</td>
                        <td>{{ app.job.title }}</td>
                        <td>
                            <span class="badge badge-{{ app.status_class }}">
                                {{ app.status }}
                            </span>
                        </td>
                        <td>{{ app.applied_at|date:"M d, Y" }}</td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="4" class="text-center text-muted">
                            No applications yet
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
{% endblock %}
```

**View Changes:**
```python
# OLD VIEW
def employer_dashboard(request):
    return render(request, 'pages/employer_dashboard.html', {
        'active_jobs_count': Job.objects.filter(employer=request.user, status='active').count(),
        'total_applications': Application.objects.filter(job__employer=request.user).count(),
        'applications': Application.objects.filter(job__employer=request.user)[:10],
    })

# NEW VIEW (Stats moved to widgets, only pass applications)
def employer_dashboard(request):
    applications = Application.objects.filter(
        job__employer=request.user
    ).select_related('candidate', 'job').order_by('-applied_at')[:10]
    
    return render(request, 'pages/employer_dashboard.html', {
        'applications': applications,
    })
```

**What Changed:**
- ✅ Removed sidebar navigation HTML (now automatic)
- ✅ Removed stat cards HTML (now widgets)
- ✅ Removed header/title duplication (in base template)
- ✅ Kept only page-specific content
- ✅ View only returns page-specific data

---

#### Example 2: Candidate Dashboard

**OLD CODE:**
```django
{# OLD: templates/pages/candidate_dashboard.html #}
{% extends 'Base/base.html' %}

{% block content %}
<div class="dashboard">
    <aside class="sidebar">
        <nav>
            <a href="{% url 'candidate_dashboard' %}">Dashboard</a>
            <a href="{% url 'job_list' %}">Find Jobs</a>
            <a href="{% url 'candidate_applications' %}">My Applications</a>
            <a href="{% url 'candidate_saved_jobs' %}">Saved Jobs</a>
        </nav>
    </aside>
    
    <main>
        <h1>Welcome, {{ user.profile.full_name }}</h1>
        
        <div class="stats">
            <div>Applied: {{ applications_count }}</div>
            <div>Saved: {{ saved_jobs_count }}</div>
        </div>
        
        <div class="recommended-jobs">
            <h2>Recommended Jobs</h2>
            {% for job in recommended_jobs %}
                <div class="job-card">{{ job.title }}</div>
            {% endfor %}
        </div>
    </main>
</div>
{% endblock %}
```

**NEW CODE:**
```django
{# NEW: templates/pages/candidate_dashboard.html #}
{% extends 'Base/dashboard_base.html' %}

{% block title %}My Dashboard - Jobstock{% endblock %}

{% block page_title %}Welcome, {{ user.profile.full_name }}!{% endblock %}
{% block page_description %}
    <p class="page-description">Find your next opportunity</p>
{% endblock %}

{% block content %}
    <!-- Stats are automatic via widgets -->
    
    <!-- Recommended Jobs (page-specific content) -->
    <div class="card">
        <div class="card-header">
            <h5>
                <i class="fas fa-star"></i>
                Recommended For You
            </h5>
        </div>
        <div class="card-body">
            <div class="row">
                {% for job in recommended_jobs %}
                <div class="col-md-6 mb-3">
                    <div class="job-card">
                        <h6>{{ job.title }}</h6>
                        <p class="text-muted">{{ job.company_name }}</p>
                        <div class="job-meta">
                            <span><i class="fas fa-map-marker-alt"></i> {{ job.location }}</span>
                            <span><i class="fas fa-dollar-sign"></i> {{ job.salary_range }}</span>
                        </div>
                        <a href="{% url 'job_detail' job.id %}" class="btn btn-sm btn-primary mt-2">
                            View Details
                        </a>
                    </div>
                </div>
                {% empty %}
                <div class="col-12">
                    <p class="text-muted text-center">No recommendations yet. Update your profile to get better matches!</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
{% endblock %}
```

---

#### Example 3: RPO Admin Dashboard

**NEW CODE:**
```django
{# templates/pages/rpo_dashboard.html #}
{% extends 'Base/dashboard_base.html' %}

{% block title %}RPO Admin Dashboard{% endblock %}

{% block page_title %}RPO Admin Dashboard{% endblock %}
{% block page_description %}
    <p class="page-description">Manage clients and recruitment operations</p>
{% endblock %}

{% block content %}
    <!-- Client Performance Chart -->
    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h5>Client Performance</h5>
                </div>
                <div class="card-body">
                    <canvas id="clientPerformanceChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h5>Recent Activities</h5>
                </div>
                <div class="card-body">
                    <ul class="activity-list">
                        {% for activity in recent_activities %}
                        <li>
                            <strong>{{ activity.client_name }}</strong>
                            {{ activity.description }}
                            <small class="text-muted">{{ activity.timestamp|timesince }} ago</small>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </div>
    </div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    // Chart initialization
    const ctx = document.getElementById('clientPerformanceChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: {{ client_labels|safe }},
            datasets: [{
                label: 'Placements',
                data: {{ placement_data|safe }},
                backgroundColor: 'rgba(54, 162, 235, 0.5)'
            }]
        }
    });
</script>
{% endblock %}
```

---

## Migration Checklist

### For Each Template:

- [ ] Remove hardcoded navigation HTML
- [ ] Remove duplicate header/title elements
- [ ] Change `{% extends 'Base/base.html' %}` to `{% extends 'Base/dashboard_base.html' %}`
- [ ] Move page title to `{% block page_title %}`
- [ ] Move page description to `{% block page_description %}`
- [ ] Keep only page-specific content in `{% block content %}`
- [ ] Remove stat cards (now handled by widgets)
- [ ] Update CSS classes to match Bootstrap 5
- [ ] Test with all user roles

### For Each View:

- [ ] Remove navigation context data
- [ ] Remove stat calculations (moved to widget APIs)
- [ ] Keep only page-specific data
- [ ] Use service layer instead of direct ORM queries
- [ ] Return standardized response format

---

## Comparison Table

| Feature | Before | After |
|---------|--------|-------|
| **Navigation** | Hardcoded in each template | Database-driven, automatic |
| **User Roles** | Manual if/else checks | Automatic filtering |
| **Stats/Widgets** | Duplicated in every view | Reusable widget components |
| **URLs** | Hardcoded paths | Django URL names |
| **Updates** | Change multiple files | Update database |
| **Customization** | Edit templates | User preferences |
| **Code Lines** | ~200 per template | ~50 per template |

---

## Common Patterns

### Pattern 1: Replace Hardcoded Stats

**Before:**
```python
def dashboard(request):
    context = {
        'active_jobs': Job.objects.filter(status='active').count(),
        'pending_apps': Application.objects.filter(status='pending').count(),
    }
    return render(request, 'dashboard.html', context)
```

**After:**
```python
# Stats moved to widget API endpoint
@api_view(['GET'])
def get_active_jobs_count(request):
    count = Job.objects.filter(status='active').count()
    return DRFResponse.success(data={'count': count})

# View only returns page-specific data
def dashboard(request):
    # Widgets load automatically via dashboard_base.html
    return render(request, 'dashboard.html')
```

### Pattern 2: Replace Hardcoded Navigation

**Before:**
```django
<nav>
    {% if user.profile.role == 'hiring_manager' %}
        <a href="/employer/dashboard/">Dashboard</a>
        <a href="/employer/jobs/">Jobs</a>
    {% elif user.profile.role == 'candidate' %}
        <a href="/candidate/dashboard/">Dashboard</a>
        <a href="/jobs/">Find Jobs</a>
    {% endif %}
</nav>
```

**After:**
```django
{# Navigation automatic in dashboard_base.html #}
{# Just extend the base template #}
{% extends 'Base/dashboard_base.html' %}
```

---

## Testing After Migration

### 1. Test Each User Role

```bash
# Login as each role and verify:
- ✅ Correct navigation items shown
- ✅ Correct widgets displayed
- ✅ Correct quick actions available
- ✅ No permission errors
```

### 2. Test Navigation

```bash
- ✅ Click every navigation link
- ✅ Verify active state highlights current page
- ✅ Test submenu expand/collapse
- ✅ Test mobile responsive menu
```

### 3. Test Widgets

```bash
- ✅ Widgets load data correctly
- ✅ Refresh button works
- ✅ Hide button works
- ✅ Custom widget order persists
```

---

## Rollback Plan

If migration causes issues:

1. **Keep old templates as backup**:
   ```bash
   cp templates/pages/employer_dashboard.html templates/pages/employer_dashboard.html.backup
   ```

2. **Revert settings.py** if needed:
   ```python
   # Remove this line from context_processors:
   # "App.context_processors_navigation.navigation_context",
   ```

3. **Switch back to old template**:
   ```bash
   mv templates/pages/employer_dashboard.html.backup templates/pages/employer_dashboard.html
   ```

---

## Performance Considerations

### Cache Navigation Data

```python
# In context processor
from django.core.cache import cache

def navigation_context(request):
    if request.user.is_authenticated:
        cache_key = f'nav_{request.user.id}'
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        result = NavigationService.get_complete_dashboard_data(request.user)
        cache.set(cache_key, result, 3600)  # 1 hour
        return result
```

### Optimize Database Queries

```python
# Use select_related and prefetch_related
NavigationGroup.objects.filter(
    is_active=True
).prefetch_related(
    'items',
    'items__children'
)
```

---

## Summary

**Before Migration:**
- 200+ lines per template
- Hardcoded navigation in every file
- Manual role checks everywhere
- Difficult to maintain

**After Migration:**
- 50 lines per template
- Database-driven navigation
- Automatic role filtering
- Easy to maintain

**Result:**
- ✅ 75% less code
- ✅ Centralized configuration
- ✅ Easier updates
- ✅ Better UX consistency
