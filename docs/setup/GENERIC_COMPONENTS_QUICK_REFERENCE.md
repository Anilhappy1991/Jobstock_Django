# Quick Reference: Using Generic Components in Other Modules

## 1. Generic Form (Reusable in Any Module)

```python
# In any app's forms.py
from App.forms import BaseModelForm

class EmployerProfileForm(BaseModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'industry', 'website']
        # That's it! Auto-gets form-control classes and placeholders
```

## 2. Generic Messages (Reusable Everywhere)

```python
# In any view
from App.utils import MessageMixin

def my_view(request):
    # Show success message
    MessageMixin.success_message(request, "Operation successful!")
    
    # Show error message
    MessageMixin.error_message(request, "Something went wrong")
    
    # Show warning
    MessageMixin.warning_message(request, "Please review your input")
    
    # Show info
    MessageMixin.info_message(request, "Helpful information here")
```

## 3. Generic Form Handler (Reusable Everywhere)

```python
# In any view
from App.utils import FormHandlerMixin

def my_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        
        # Single form save
        result = FormHandlerMixin.handle_form_save(
            form,
            request,
            success_message_text="Saved successfully!",
            error_message_text="Failed to save"
        )
        
        if result['success']:
            return redirect('success_page')
```

## 4. Snackbar Notifications (Reusable in Any Template)

```html
<!-- Include once in your template -->
{% include 'Components/snackbar.html' %}

<!-- Then use anywhere in JavaScript -->
<script>
    // Success
    Snackbar.success('Data saved!');
    
    // Error
    Snackbar.error('Failed to save!');
    
    // Warning
    Snackbar.warning('Please check your input');
    
    // Info
    Snackbar.info('Just so you know...');
    
    // Custom duration (ms)
    Snackbar.show('Custom message', 'success', 5000);
</script>
```

## 5. Complete View Example (Copy-Paste Template)

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from App.utils import MessageMixin, FormHandlerMixin
from .forms import YourForm
from .models import YourModel

@login_required
def your_view(request, id=None):
    # Get or create instance
    if id:
        instance = YourModel.objects.get(id=id)
    else:
        instance = None
    
    if request.method == 'POST':
        form = YourForm(request.POST, request.FILES, instance=instance)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    obj = form.save()
                    MessageMixin.success_message(request, "Saved successfully!")
                    return redirect('your_success_url', id=obj.id)
            except Exception as e:
                MessageMixin.error_message(request, f"Error: {str(e)}")
        else:
            MessageMixin.error_message(request, "Please correct the errors")
    else:
        form = YourForm(instance=instance)
    
    context = {
        'form': form,
        'instance': instance,
    }
    return render(request, 'your_template.html', context)
```

## 6. Complete Template Example (Copy-Paste Template)

```html
{% extends "Base/base.html" %}
{% load static %}

{% block hero_content %}

<!-- Include snackbar -->
{% include 'Components/snackbar.html' %}

<div class="container">
    <div class="card">
        <div class="card-header">
            <h4>Your Form Title</h4>
        </div>
        <div class="card-body">
            <form method="POST" enctype="multipart/form-data">
                {% csrf_token %}
                
                <div class="row">
                    {% for field in form %}
                    <div class="col-md-6">
                        <div class="form-group">
                            <label>{{ field.label }}</label>
                            {{ field }}
                            {% if field.errors %}
                                <div class="text-danger small">
                                    {{ field.errors }}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                    {% endfor %}
                    
                    <div class="col-12">
                        <button type="submit" class="btn btn-primary">
                            Save
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>

<!-- Optional: Custom JavaScript -->
<script>
    document.querySelector('form').addEventListener('submit', function(e) {
        // Add loading state
        const btn = this.querySelector('button[type="submit"]');
        btn.disabled = true;
        btn.innerHTML = 'Saving...';
    });
</script>

{% endblock %}
```

## 7. AJAX Form Submission (Optional Enhancement)

```html
<script>
    // AJAX form submission with snackbar
    document.querySelector('form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Snackbar.success(data.message);
                // Optional: redirect or update UI
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                Snackbar.error(data.message);
            }
        })
        .catch(error => {
            Snackbar.error('An error occurred. Please try again.');
        });
    });
</script>
```

## 8. Dropdown Usage (Database-Driven)

```python
# In your form
from App.models import DropdownMaster

class YourForm(BaseModelForm):
    industry = forms.ModelChoiceField(
        queryset=DropdownMaster.objects.filter(
            group__text='Industry', 
            is_active=True
        ),
        empty_label="Select Industry"
    )
    
    class Meta:
        model = YourModel
        fields = ['name', 'industry']
```

## 9. Adding New Dropdown Category

```python
# In Django shell or management command
from App.models import DropdownGroup, DropdownMaster

# Create group
group = DropdownGroup.objects.create(
    text='Job Type',
    value='Job Type'
)

# Add items
items = ['Full Time', 'Part Time', 'Contract', 'Freelance']
for i, item in enumerate(items, 1):
    DropdownMaster.objects.create(
        group=group,
        text=item,
        value=item,
        sort_order=i
    )
```

## 10. Profile Completion Calculation (Auto)

```python
# In your model
class YourModel(models.Model):
    # ... fields ...
    completion = models.IntegerField(default=0)
    
    def calculate_completion(self):
        fields = [self.field1, self.field2, self.field3]
        filled = sum(1 for f in fields if f)
        return int((filled / len(fields)) * 100)
    
    def save(self, *args, **kwargs):
        self.completion = self.calculate_completion()
        super().save(*args, **kwargs)
```

## 11. Permission Checking Template

```python
from django.contrib.auth.decorators import login_required

@login_required
def your_view(request, username):
    user = get_object_or_404(User, username=username)
    
    # Check permission
    if request.user != user and not request.user.is_staff:
        MessageMixin.error_message(
            request, 
            "You don't have permission"
        )
        return redirect('home')
    
    # Continue with view logic...
```

## 12. Multiple Forms in One Page

```html
<!-- Form 1: Basic Info -->
<form method="POST">
    {% csrf_token %}
    <input type="hidden" name="form_type" value="basic">
    <!-- fields -->
    <button type="submit">Save Basic Info</button>
</form>

<!-- Form 2: Contact Info -->
<form method="POST">
    {% csrf_token %}
    <input type="hidden" name="form_type" value="contact">
    <!-- fields -->
    <button type="submit">Save Contact Info</button>
</form>
```

```python
# In view
form_type = request.POST.get('form_type', 'basic')

if form_type == 'basic':
    form = BasicForm(request.POST, instance=profile)
elif form_type == 'contact':
    form = ContactForm(request.POST, instance=profile)
    
if form.is_valid():
    form.save()
    MessageMixin.success_message(request, "Saved!")
```

## Summary

**3 Generic Components = Infinite Reusability**

1. **BaseModelForm** - Use for all forms
2. **MessageMixin** - Use for all messages
3. **Snackbar Component** - Include in all templates

**Copy-paste these patterns anywhere in your project!**
