from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    Profile, CandidateSkill, CandidateEducation, 
    CandidateExperience, CandidateCertification, DropdownMaster
)

WORK_STATUS_CHOICES = (
    ('findjob', "I'm looking for a job"),
    ('findtalent', "I'm looking for talent"),
)

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username (no @)'
        })
    )
    full_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'What is your name?'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder':'Tell us your Email ID'
        })
    )
    phone = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Enter your mobile number'
        })
    )
    work_status = forms.ChoiceField(
        choices=WORK_STATUS_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'(Minimum 8 characters)'}),
        help_text="",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password'}),
        help_text="",
    )

    class Meta:
        model = User
        fields = ('username', 'full_name','email','phone','work_status','password1','password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure username is visible and required
        self.fields['username'].required = True
        # password1 and password2 are part of UserCreationForm but we override styling
        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'class':'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set username from form field and save email
        username = self.cleaned_data.get('username')
        user.username = username
        user.email = self.cleaned_data.get('email')
        full_name = self.cleaned_data.get('full_name')
        if full_name:
            parts = full_name.split(None, 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                full_name=full_name,
                phone=self.cleaned_data.get('phone'),
                work_status=self.cleaned_data.get('work_status')
            )
        return user

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Username is required')
        if '@' in username:
            raise forms.ValidationError("Username must not contain '@' characters.")
        # Check for uniqueness
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        # No special processing required; ensure user-supplied username is used
        return cleaned_data


class RoleAssignForm(forms.Form):
    username = forms.CharField(widget=forms.HiddenInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


# ============== GENERIC BASE FORM ==============
class BaseModelForm(forms.ModelForm):
    """Generic base form with common functionality"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class to all fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, 
                                        forms.NumberInput, forms.Textarea, 
                                        forms.Select, forms.URLInput, forms.DateInput)):
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'
            
            # Add placeholders from field labels
            if not field.widget.attrs.get('placeholder') and field.label:
                field.widget.attrs['placeholder'] = f"Enter {field.label}"
    
    def save(self, commit=True):
        """Generic save with error handling"""
        try:
            instance = super().save(commit=commit)
            return instance
        except Exception as e:
            raise forms.ValidationError(f"Error saving data: {str(e)}")


# ============== CANDIDATE PROFILE FORMS ==============
class CandidateProfileBasicForm(BaseModelForm):
    """Form for basic profile information"""
    
    class Meta:
        model = Profile
        fields = [
            'full_name', 'job_title', 'age', 'education', 'experience',
            'languages', 'about'
        ]
        widgets = {
            'about': forms.Textarea(attrs={'rows': 4, 'class': 'form-control ht-80'}),
            'education': forms.Select(attrs={'class': 'form-control'}),
            'experience': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'full_name': 'Your Name',
            'job_title': 'Job Title',
            'age': 'Age',
            'education': 'Education',
            'experience': 'Experience',
            'languages': 'Languages',
            'about': 'About Info',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set queryset for dropdown fields
        self.fields['education'].queryset = DropdownMaster.objects.filter(
            group__text='Education', is_active=True
        )
        self.fields['education'].empty_label = "Select Education"
        
        self.fields['experience'].queryset = DropdownMaster.objects.filter(
            group__text='Experience', is_active=True
        )
        self.fields['experience'].empty_label = "Select Experience"


class CandidateProfileContactForm(BaseModelForm):
    """Form for contact details"""
    
    class Meta:
        model = Profile
        fields = [
            'email', 'phone', 'temp_address', 'address', 'address2',
            'country', 'city', 'zip_code', 'latitude', 'longitude'
        ]
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'email': 'Your Email',
            'phone': 'Phone No.',
            'temp_address': 'Temporary Address',
            'address': 'Address',
            'address2': 'Address 2',
            'country': 'Country',
            'city': 'State/City',
            'zip_code': 'Zip Code',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set queryset for dropdown fields
        self.fields['country'].queryset = DropdownMaster.objects.filter(
            group__text='Country', is_active=True
        )
        self.fields['country'].empty_label = "Select Country"
        
        self.fields['city'].queryset = DropdownMaster.objects.filter(
            group__text='State/City', is_active=True
        )
        self.fields['city'].empty_label = "Select State/City"


class CandidateProfileSocialForm(BaseModelForm):
    """Form for social links"""
    
    class Meta:
        model = Profile
        fields = ['facebook', 'twitter', 'instagram', 'linkedin', 'google_plus']
        labels = {
            'facebook': 'Facebook',
            'twitter': 'Twitter',
            'instagram': 'Instagram',
            'linkedin': 'Linked In',
            'google_plus': 'Google Plus',
        }


class CandidateSkillForm(BaseModelForm):
    """Form for adding skills"""
    
    class Meta:
        model = CandidateSkill
        fields = ['skill_name', 'proficiency']
        widgets = {
            'proficiency': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'skill_name': 'Skill Name',
            'proficiency': 'Proficiency Level',
        }


class CandidateEducationForm(BaseModelForm):
    """Form for education history"""
    
    class Meta:
        model = CandidateEducation
        fields = ['degree', 'institution', 'field_of_study', 'start_date', 'end_date', 'is_current', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'degree': 'Degree',
            'institution': 'Institution/University',
            'field_of_study': 'Field of Study',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'is_current': 'Currently Studying',
            'description': 'Description',
        }


class CandidateExperienceForm(BaseModelForm):
    """Form for work experience"""
    
    class Meta:
        model = CandidateExperience
        fields = ['job_title', 'company_name', 'location', 'start_date', 'end_date', 'is_current', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'job_title': 'Job Title',
            'company_name': 'Company Name',
            'location': 'Location',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'is_current': 'Currently Working',
            'description': 'Job Description',
        }


class CandidateCertificationForm(BaseModelForm):
    """Form for certifications"""
    
    class Meta:
        model = CandidateCertification
        fields = ['certification_name', 'issuing_organization', 'issue_date', 'expiry_date', 'credential_id', 'credential_url']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'certification_name': 'Certification Name',
            'issuing_organization': 'Issuing Organization',
            'issue_date': 'Issue Date',
            'expiry_date': 'Expiry Date',
            'credential_id': 'Credential ID',
            'credential_url': 'Credential URL',
        }

