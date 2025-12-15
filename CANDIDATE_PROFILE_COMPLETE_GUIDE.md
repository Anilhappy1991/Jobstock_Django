# Candidate Profile System - Complete Implementation Guide

## Overview
This document describes the complete, production-ready candidate profile system with normalized database design, generic reusable components, and snackbar notifications.

## Architecture

### Database Schema (Normalized)

```
┌─────────────────────┐
│   User (Django)     │
│   - username        │
│   - email           │
│   - password        │
└──────┬──────────────┘
       │ 1:1
       ▼
┌─────────────────────────────────┐
│   Profile (user_profile)        │
│   Main Profile Information       │
├─────────────────────────────────┤
│ - user_id (FK)                  │
│ - full_name                     │
│ - job_title                     │
│ - age                           │
│ - education_id (FK)             │◄──┐
│ - experience_id (FK)            │◄──┤
│ - languages                     │   │
│ - about                         │   │
│ - email, phone, addresses       │   │
│ - country_id (FK)               │◄──┤
│ - city_id (FK)                  │◄──┤
│ - social_links                  │   │
│ - profile_image, resume         │   │
│ - profile_completion            │   │
│ - is_active                     │   │
│ - created_at, updated_at        │   │
└──┬──────────────────────────────┘   │
   │                                   │
   │ 1:N                               │
   ├──────────┐                        │
   │          │                        │
   ▼          ▼                        │
┌────────┐ ┌────────────┐             │
│Skills  │ │ Education  │             │
│        │ │ History    │             │
└────────┘ └────────────┘             │
   ▼          ▼                        │
┌────────┐ ┌────────────┐             │
│Experience Certificate │             │
│        │ │            │             │
└────────┘ └────────────┘             │
                                      │
┌─────────────────────┐               │
│  dropdown_group     │               │
├─────────────────────┤               │
│ - id               │                │
│ - text             │                │
│ - value            │                │
└──────┬──────────────┘               │
       │ 1:N                          │
       ▼                              │
┌─────────────────────┐               │
│  dropdown_master    │───────────────┘
├─────────────────────┤
│ - id               │
│ - group_id (FK)    │
│ - text             │
│ - value            │
│ - sort_order       │
└─────────────────────┘
```

## Models Created

### 1. Profile (Extended)
- **Table:** `user_profile`
- **Purpose:** Main candidate profile with all basic information
- **Features:**
  - Auto-calculates profile completion percentage
  - Foreign keys to dropdown masters for Education, Experience, Country, City
  - Timestamps for created/updated tracking
  - Image and resume file uploads

### 2. CandidateSkill
- **Table:** `candidate_skills`
- **Purpose:** Store candidate skills with proficiency levels
- **Relationship:** Many skills per profile

### 3. CandidateEducation
- **Table:** `candidate_education`
- **Purpose:** Education history with degrees and institutions
- **Features:** Date range tracking, current education flag

### 4. CandidateExperience
- **Table:** `candidate_experience`
- **Purpose:** Work experience history
- **Features:** Job titles, companies, date ranges, descriptions

### 5. CandidateCertification
- **Table:** `candidate_certification`
- **Purpose:** Professional certifications
- **Features:** Credential IDs, URLs, expiry tracking

## Generic Components Created

### 1. BaseModelForm (App/forms.py)
Generic base form class that can be reused across all modules:

```python
class BaseModelForm(forms.ModelForm):
    """
    Generic base form with common functionality:
    - Auto-adds form-control CSS class
    - Auto-generates placeholders
    - Generic save with error handling
    """
```

**Usage in Other Modules:**
```python
from App.forms import BaseModelForm

class YourCustomForm(BaseModelForm):
    class Meta:
        model = YourModel
        fields = ['field1', 'field2']
```

### 2. MessageMixin (App/utils.py)
Reusable message handling:

```python
from App.utils import MessageMixin

# In any view
MessageMixin.success_message(request, "Data saved successfully!")
MessageMixin.error_message(request, "An error occurred!")
MessageMixin.warning_message(request, "Please review your input")
MessageMixin.info_message(request, "Information message")
```

### 3. FormHandlerMixin (App/utils.py)
Generic form save handler:

```python
from App.utils import FormHandlerMixin

# Handle single form
result = FormHandlerMixin.handle_form_save(
    form, 
    request, 
    success_message_text="Saved!",
    error_message_text="Error saving"
)

# Handle multiple forms at once
forms_dict = {
    'basic': form_basic,
    'contact': form_contact,
}
result = FormHandlerMixin.handle_multiple_forms(
    forms_dict, 
    request, 
    success_message="All data saved!"
)
```

### 4. Snackbar Component (templates/Components/snackbar.html)
Reusable notification system:

**Include in any template:**
```html
{% include 'Components/snackbar.html' %}
```

**Use in JavaScript:**
```javascript
// Success notification
Snackbar.success('Profile updated successfully!');

// Error notification
Snackbar.error('Failed to save data');

// Warning notification
Snackbar.warning('Please fill required fields');

// Info notification
Snackbar.info('Your session will expire soon');

// Custom duration
Snackbar.show('Message', 'success', 5000); // 5 seconds

// No auto-close
Snackbar.show('Stays forever', 'info', 0);
```

**Auto-shows Django messages:**
The snackbar automatically displays any Django messages (success, error, warning, info) without additional code.

## Forms Created

### Basic Forms
1. **CandidateProfileBasicForm** - Name, job title, age, education, experience, languages, about
2. **CandidateProfileContactForm** - Email, phone, addresses, country, city, coordinates
3. **CandidateProfileSocialForm** - Facebook, Twitter, Instagram, LinkedIn, Google+

### Related Model Forms
4. **CandidateSkillForm** - Add/edit skills
5. **CandidateEducationForm** - Add/edit education history
6. **CandidateExperienceForm** - Add/edit work experience
7. **CandidateCertificationForm** - Add/edit certifications

All forms extend `BaseModelForm` for consistency.

## View Implementation

### candidate_profile_detail View
**Features:**
- Login required
- Permission checking (users can only edit their own profile)
- Handles three separate forms (basic, contact, social)
- Transaction-based saves
- Automatic success/error messages
- Redirects after successful save
- Auto-calculates profile completion

**Form Handling:**
```python
# Each form has a hidden field: form_type
# This identifies which form was submitted
form_type = request.POST.get('form_type', 'basic')

if form_type == 'basic':
    # Handle basic form
elif form_type == 'contact':
    # Handle contact form
elif form_type == 'social':
    # Handle social form
```

## Template Updates

### Form Structure
Each section has its own form with:
- CSRF token
- Hidden field identifying form type
- Form fields with error display
- Submit button

**Example:**
```html
<form method="POST" action="">
    {% csrf_token %}
    <input type="hidden" name="form_type" value="basic">
    
    <div class="form-group">
        <label>{{ form_basic.full_name.label }}</label>
        {{ form_basic.full_name }}
        {% if form_basic.full_name.errors %}
            <div class="text-danger small">
                {{ form_basic.full_name.errors }}
            </div>
        {% endif %}
    </div>
    
    <button type="submit">Save</button>
</form>
```

## How to Use in Other Modules

### 1. Create a Model Form
```python
from App.forms import BaseModelForm
from .models import YourModel

class YourModelForm(BaseModelForm):
    class Meta:
        model = YourModel
        fields = ['field1', 'field2', 'field3']
        widgets = {
            'field1': forms.TextInput(attrs={'placeholder': 'Custom placeholder'}),
        }
```

### 2. Create a View
```python
from App.utils import MessageMixin, FormHandlerMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction

@login_required
def your_view(request):
    instance = YourModel.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = YourModelForm(request.POST, instance=instance)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    MessageMixin.success_message(request, "Data saved successfully!")
                    return redirect('your_success_url')
            except Exception as e:
                MessageMixin.error_message(request, f"Error: {str(e)}")
        else:
            MessageMixin.error_message(request, "Please correct the errors")
    else:
        form = YourModelForm(instance=instance)
    
    return render(request, 'your_template.html', {'form': form})
```

### 3. Create a Template
```html
{% extends "Base/base.html" %}
{% load static %}

{% block hero_content %}
{% include 'Components/snackbar.html' %}

<div class="card">
    <div class="card-body">
        <form method="POST">
            {% csrf_token %}
            
            {% for field in form %}
            <div class="form-group">
                <label>{{ field.label }}</label>
                {{ field }}
                {% if field.errors %}
                    <div class="text-danger small">{{ field.errors }}</div>
                {% endif %}
            </div>
            {% endfor %}
            
            <button type="submit" class="btn btn-primary">Save</button>
        </form>
    </div>
</div>

<script>
// Optional: Custom JavaScript interactions
document.querySelector('form').addEventListener('submit', function(e) {
    // Custom validation or processing
});
</script>

{% endblock %}
```

## Testing

### 1. Start the Server
```bash
python manage.py runserver
```

### 2. Login and Navigate
```
http://localhost:8000/candidate-profile/
```

### 3. Test Each Form
- Fill out basic details → Submit → Check for snackbar notification
- Fill out contact details → Submit → Check for snackbar notification
- Fill out social links → Submit → Check for snackbar notification

### 4. Verify Database
```bash
python manage.py dbshell
```

```sql
-- Check profile data
SELECT * FROM user_profile;

-- Check skills
SELECT * FROM candidate_skills;

-- Check profile completion
SELECT user_id, full_name, profile_completion FROM user_profile;
```

## Admin Interface

All models are registered in Django admin with:
- List displays
- Filters
- Search functionality
- Inline editing where appropriate

Access at: `http://localhost:8000/admin/`

## API Endpoints (Future Enhancement)

The generic structure makes it easy to add REST API endpoints:

```python
# Example DRF ViewSet
from rest_framework import viewsets
from .models import Profile
from .serializers import ProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def perform_update(self, serializer):
        serializer.save()
        # Auto-calculate profile completion
        serializer.instance.save()
```

## Security Features

1. **Login Required:** Views decorated with `@login_required`
2. **Permission Checking:** Users can only edit their own profiles
3. **Transaction Safety:** All saves wrapped in `transaction.atomic()`
4. **CSRF Protection:** All forms include CSRF tokens
5. **Validation:** Form validation before saving
6. **Error Handling:** Try-except blocks for graceful error handling

## Performance Optimizations

1. **Select Related:** Use `select_related()` for foreign keys
2. **Prefetch Related:** Use `prefetch_related()` for reverse relations
3. **Indexing:** Key fields indexed in Meta classes
4. **Lazy Loading:** Forms instantiated only when needed

## Reusability Checklist

✅ Generic base form class
✅ Generic utility mixins
✅ Reusable snackbar component
✅ Consistent error handling
✅ Normalized database design
✅ Documented code
✅ Admin interface configured
✅ Transaction safety
✅ Permission checking
✅ Mobile responsive

## Migration Summary

**Created:**
- 0005: Added DropdownGroup and DropdownMaster
- 0006: Extended Profile with all fields + 4 related models

**Tables:**
- `user_profile` (main profile)
- `candidate_skills`
- `candidate_education`
- `candidate_experience`
- `candidate_certification`
- `dropdown_group`
- `dropdown_master`

## Files Modified/Created

### Models
- ✅ App/models.py - Extended Profile, added related models

### Forms
- ✅ App/forms.py - Added 7 forms with BaseModelForm

### Views
- ✅ App/views.py - Updated candidate_profile_detail with form handling

### Templates
- ✅ templates/pages/candidate-profile.html - Added forms with proper handling
- ✅ templates/Components/snackbar.html - Reusable notification component

### Utilities
- ✅ App/utils.py - Generic mixins and helpers

### Admin
- ✅ App/admin.py - Registered all models

### Migrations
- ✅ 0005_dropdowngroup_alter_profile_options_dropdownmaster.py
- ✅ 0006_alter_profile_options_profile_about_profile_address_and_more.py

## Next Steps

1. **Add AJAX form submission** for smoother UX
2. **Add file upload handlers** for profile image and resume
3. **Create REST API** using Django REST Framework
4. **Add search and filtering** for candidates
5. **Add export functionality** (PDF, CSV)
6. **Add email notifications** on profile updates
7. **Add profile analytics** dashboard
8. **Implement profile visibility** settings

## Support

For issues or questions:
1. Check the snackbar notifications for error messages
2. Check Django admin for data verification
3. Check browser console for JavaScript errors
4. Check Django logs for backend errors

---

**Version:** 1.0  
**Last Updated:** December 15, 2025  
**Status:** Production Ready ✅
