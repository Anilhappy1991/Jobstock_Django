"""
Authentication views - Login, Logout, Signup
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse

from App.forms import SignUpForm


def signup(request):
    """User registration"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('App:candidate_profile_detail', username=user.username)
    else:
        form = SignUpForm()
    return render(request, 'pages/signup.html', {'form': form})


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Debug logging
        print(f"Login attempt - Username: {username}, Password provided: {bool(password)}")
        
        user = authenticate(request=request, username=username, password=password)
        
        # Get the next URL from POST data or use HTTP_REFERER
        next_url = request.POST.get('next', '')
        if not next_url or '/login' in next_url:
            next_url = request.META.get('HTTP_REFERER', reverse('App:index'))
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            print(f"Login successful for user: {username}")
            
            # Clean the next_url - remove query parameters related to login
            if '?login=failed' in next_url:
                next_url = next_url.replace('?login=failed', '')
            if '&login=failed' in next_url:
                next_url = next_url.replace('&login=failed', '')
            
            # Determine redirect based on user role if no next_url
            if not next_url or next_url == reverse('App:index'):
                # Get user's role from profile or group
                user_role = None
                try:
                    user_role = user.profile.role
                except:
                    # Fallback to checking groups
                    if user.groups.filter(name__icontains='hiring').exists() or user.groups.filter(name='Hiring Managers').exists():
                        user_role = 'hiring_manager'
                    elif user.groups.filter(name__icontains='candidate').exists() or user.groups.filter(name='Candidates').exists():
                        user_role = 'candidate'
                    elif user.groups.filter(name__icontains='rpo').exists():
                        user_role = 'rpo_admin'
                
                # Redirect to appropriate dashboard
                if user_role == 'hiring_manager' or user.is_superuser:
                    next_url = reverse('App:employer_dashboard')
                elif user_role == 'candidate':
                    next_url = reverse('App:candidate_dashboard')
                elif user_role == 'rpo_admin':
                    next_url = reverse('App:employer_dashboard')  # RPO uses employer dashboard
                else:
                    # Default to index if role is unknown
                    next_url = reverse('App:index')
            
            # Redirect to the next URL
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            print(f"Login failed for username: {username}")
            
            # Redirect back to the referring page with error flag
            redirect_url = next_url if next_url else reverse('App:index')
            
            # Add login=failed parameter to reopen the modal
            separator = '&' if '?' in redirect_url else '?'
            return redirect(f"{redirect_url}{separator}login=failed")
    
    # For GET requests, just redirect to index
    return redirect('App:index')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('App:index')
