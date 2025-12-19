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
        user = authenticate(request, username=username, password=password)
        
        # Try to use next from POST, fall back to HTTP_REFERER or index
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('App:index')
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            # Redirect to the user's profile using their email
            return redirect('App:candidate_profile_detail', username=user.email)
        else:
            messages.error(request, 'Invalid username or password.')
            # On failure, redirect to the same page and open login modal
            if '?' in next_url:
                return redirect(f"{next_url}&login=failed")
            return redirect(f"{next_url}?login=failed")
    
    # For GET or other, just redirect to index
    return redirect('App:index')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('App:index')
