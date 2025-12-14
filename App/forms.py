from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

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
