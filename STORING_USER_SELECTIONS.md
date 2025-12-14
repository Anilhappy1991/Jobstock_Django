# How to Store User's Dropdown Selections

## Overview
This guide shows how to extend the Profile model to store user's selections from dropdowns.

## Step 1: Update Profile Model

Add these fields to the `Profile` model in `App/models.py`:

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    work_status = models.CharField(max_length=20, choices=WORK_STATUS_CHOICES, default='findjob')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')
    
    # NEW FIELDS FOR DROPDOWN SELECTIONS
    job_title = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(null=True, blank=True)
    education = models.ForeignKey(
        'DropdownMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='education_profiles',
        limit_choices_to={'group__text': 'Education'}
    )
    experience = models.ForeignKey(
        'DropdownMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='experience_profiles',
        limit_choices_to={'group__text': 'Experience'}
    )
    language = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)
    
    # Contact Details
    email = models.EmailField(blank=True)
    temp_address = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    address2 = models.CharField(max_length=500, blank=True)
    country = models.ForeignKey(
        'DropdownMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='country_profiles',
        limit_choices_to={'group__text': 'Country'}
    )
    city = models.ForeignKey(
        'DropdownMaster', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='city_profiles',
        limit_choices_to={'group__text': 'State/City'}
    )
    zip_code = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Social Links
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    google_plus = models.URLField(blank=True)
```

## Step 2: Create and Run Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 3: Create Profile Form

Create a new form in `App/forms.py`:

```python
from .models import DropdownMaster

class CandidateProfileForm(forms.ModelForm):
    # For dropdowns, we'll use the ID
    education = forms.ModelChoiceField(
        queryset=DropdownMaster.objects.filter(group__text='Education', is_active=True),
        required=False,
        empty_label="Select Education"
    )
    experience = forms.ModelChoiceField(
        queryset=DropdownMaster.objects.filter(group__text='Experience', is_active=True),
        required=False,
        empty_label="Select Experience"
    )
    country = forms.ModelChoiceField(
        queryset=DropdownMaster.objects.filter(group__text='Country', is_active=True),
        required=False,
        empty_label="Select Country"
    )
    city = forms.ModelChoiceField(
        queryset=DropdownMaster.objects.filter(group__text='State/City', is_active=True),
        required=False,
        empty_label="Select State/City"
    )
    
    class Meta:
        model = Profile
        fields = [
            'full_name', 'job_title', 'age', 'education', 'experience',
            'language', 'about', 'email', 'phone', 'temp_address',
            'address', 'address2', 'country', 'city', 'zip_code',
            'latitude', 'longitude', 'facebook', 'twitter',
            'instagram', 'linkedin', 'google_plus'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control ht-80'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'temp_address': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'address2': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'google_plus': forms.URLInput(attrs={'class': 'form-control'}),
        }
```

## Step 4: Update View to Handle Form Submission

Update `candidate_profile_detail` view in `App/views.py`:

```python
from .forms import CandidateProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def candidate_profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('App:candidate_profile_detail', username=username)
    else:
        form = CandidateProfileForm(instance=profile)
    
    # Get dropdown items for the template
    education_items = DropdownMaster.objects.filter(group__text='Education', is_active=True)
    experience_items = DropdownMaster.objects.filter(group__text='Experience', is_active=True)
    country_items = DropdownMaster.objects.filter(group__text='Country', is_active=True)
    city_items = DropdownMaster.objects.filter(group__text='State/City', is_active=True)
    
    context = {
        'profile_user': user,
        'profile': profile,
        'form': form,
        'education_items': education_items,
        'experience_items': experience_items,
        'country_items': country_items,
        'city_items': city_items,
    }
    
    return render(request, 'pages/candidate-profile.html', context)
```

## Step 5: Update Template to Use Form

Update `candidate-profile.html`:

```html
<form method="POST" action="">
    {% csrf_token %}
    
    <div class="col-xl-6 col-lg-6 col-md-12">
        <div class="form-group">
            <label>Your Name</label>
            {{ form.full_name }}
        </div>
    </div>
    
    <div class="col-xl-6 col-lg-6 col-md-12">
        <div class="form-group">
            <label>Job Title</label>
            {{ form.job_title }}
        </div>
    </div>
    
    <div class="col-xl-6 col-lg-6 col-md-12">
        <div class="form-group">
            <label>Age</label>
            {{ form.age }}
        </div>
    </div>
    
    <div class="col-xl-6 col-lg-6 col-md-12">
        <div class="form-group">
            <label>Education</label>
            <div class="select-ops">
                <select name="education" class="form-control">
                    <option value="">Select Education</option>
                    {% for item in education_items %}
                    <option value="{{ item.id }}" {% if profile.education_id == item.id %}selected{% endif %}>
                        {{ item.text }}
                    </option>
                    {% endfor %}
                </select>
            </div>
        </div>
    </div>
    
    <div class="col-xl-6 col-lg-6 col-md-12">
        <div class="form-group">
            <label>Experience</label>
            <div class="select-ops">
                <select name="experience" class="form-control">
                    <option value="">Select Experience</option>
                    {% for item in experience_items %}
                    <option value="{{ item.id }}" {% if profile.experience_id == item.id %}selected{% endif %}>
                        {{ item.text }}
                    </option>
                    {% endfor %}
                </select>
            </div>
        </div>
    </div>
    
    <!-- Submit Button -->
    <div class="col-lg-12 col-md-12">
        <button type="submit" class="btn ft--medium btn-main">Save Profile</button>
    </div>
</form>
```

## Step 6: Displaying Selected Values

To display the user's selected education/experience values elsewhere:

```html
<!-- In any template where you have the profile object -->
{% if profile.education %}
    <p>Education: {{ profile.education.text }}</p>
{% endif %}

{% if profile.experience %}
    <p>Experience: {{ profile.experience.text }}</p>
{% endif %}

{% if profile.country %}
    <p>Country: {{ profile.country.text }}</p>
{% endif %}

{% if profile.city %}
    <p>City: {{ profile.city.text }}</p>
{% endif %}
```

## Benefits of Using ForeignKey

1. **Data Integrity**: If dropdown values change, all profiles reference the correct data
2. **Easy Filtering**: Can filter profiles by education, experience, etc.
3. **Reporting**: Can count how many candidates have each education level
4. **No Duplicate Data**: Stores only the reference ID, not the full text

## Alternative: Storing as CharField

If you prefer to store the value as text instead of ForeignKey:

```python
class Profile(models.Model):
    # ... other fields ...
    education = models.CharField(max_length=200, blank=True)
    experience = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
```

Then in the view:
```python
if request.method == 'POST':
    education_id = request.POST.get('education')
    if education_id:
        education_item = DropdownMaster.objects.get(id=education_id)
        profile.education = education_item.value
    profile.save()
```

## Testing

1. Login as a user
2. Go to candidate profile page
3. Select values from dropdowns
4. Click "Save Profile"
5. Check that selected values are saved in database
6. Refresh page - selected values should be pre-selected

## Querying Profiles by Dropdown Selections

```python
# Get all profiles with Bachelor's Degree
bachelors = DropdownMaster.objects.get(group__text='Education', text="Bachelor's Degree")
profiles = Profile.objects.filter(education=bachelors)

# Get all profiles with 5+ years experience
experience_5plus = DropdownMaster.objects.get(group__text='Experience', text='5+ Years')
profiles = Profile.objects.filter(experience=experience_5plus)

# Get all profiles from India
india = DropdownMaster.objects.get(group__text='Country', text='India')
profiles = Profile.objects.filter(country=india)
```

This gives you powerful filtering capabilities for your job portal!
