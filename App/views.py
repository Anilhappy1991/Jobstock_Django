from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from .models import Candidate
from .models import Employer
from .models import Job
from .forms import SignUpForm
from django.contrib.auth.models import User
from .models import Profile
from .forms import RoleAssignForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def home_2(request):
    return render(request, 'pages/home-2.html')

def home_3(request):
    return render(request, 'pages/home-3.html')

def home_4(request):
    return render(request, 'pages/home-4.html')

def home_5(request):
    return render(request, 'pages/home-5.html')

def home_6(request):
    return render(request, 'pages/home-6.html')

def home_7(request):
    return render(request, 'pages/home-7.html')

def home_8(request):
    return render(request, 'pages/home-8.html')

def home_9(request):
    return render(request, 'pages/home-9.html')

def home_10(request):
    return render(request, 'pages/home-10.html')

def home_11(request):
    return render(request, 'pages/home-11.html')

def home_12(request):
    return render(request, 'pages/home-12.html')

def grid_style_1(request):
    return render(request, 'pages/grid-style-1.html')

def grid_style_2(request):
    return render(request, 'pages/grid-style-2.html')

def grid_style_3(request):
    return render(request, 'pages/grid-style-3.html')

def grid_style_4(request):
    return render(request, 'pages/grid-style-4.html')

def grid_style_5(request):
    return render(request, 'pages/grid-style-5.html')

def full_job_grid_1(request):
    return render(request, 'pages/full-job-grid-1.html')

def full_job_grid_2(request):
    return render(request, 'pages/full-job-grid-2.html')

def list_style_1(request):
    return render(request, 'pages/list-style-1.html')

def list_style_2(request):
    return render(request, 'pages/list-style-2.html')

def list_style_3(request):
    return render(request, 'pages/list-style-3.html')

def full_job_list_1(request):
    return render(request, 'pages/full-job-list-1.html')

def full_job_list_2(request):
    return render(request, 'pages/full-job-list-2.html')

def half_map(request):
    return render(request, 'pages/half-map.html')

def half_map_2(request):
    return render(request, 'pages/half-map-2.html')

def half_map_3(request):
    return render(request, 'pages/half-map-3.html')

def half_map_list_1(request):
    return render(request, 'pages/half-map-list-1.html')

def half_map_list_2(request):
    return render(request, 'pages/half-map-list-2.html')

def candidate_grid_1(request):
    return render(request, 'pages/candidate-grid-1.html')

def candidate_grid_2(request):
    return render(request, 'pages/candidate-grid-2.html')

def candidate_list_1(request):
    return render(request, 'pages/candidate-list-1.html')

def candidate_list_2(request):
    return render(request, 'pages/candidate-list-2.html')

def candidate_half_map(request):
    return render(request, 'pages/candidate-half-map.html')

def candidate_half_map_list(request):
    return render(request, 'pages/candidate-half-map-list.html')

def single_layout_1(request):
    return render(request, 'pages/single-layout-1.html')

def single_layout_2(request):
    return render(request, 'pages/single-layout-2.html')

def single_layout_3(request):
    return render(request, 'pages/single-layout-3.html')

def single_layout_4(request):
    return render(request, 'pages/single-layout-4.html')

def single_layout_5(request):
    return render(request, 'pages/single-layout-5.html')

def single_layout_6(request):
    return render(request, 'pages/single-layout-6.html')

def candidate_list_or_default(request):
    # Get candidates from the database
    candidates = Candidate.objects.all()  # or any filter you need
    return render(request,'pages/candidate-detail.html', {'candidates': candidates})

def candidate_detail(request, title):
    candidate = get_object_or_404(Candidate, slug=title)  # Match the candidate by title (or slug, depending on how your model is set up)
    return render(request, 'pages/candidate-detail.html', {'candidate': candidate})

def candidate_detail_2(request):
    return render(request, 'pages/candidate-detail-2.html')

def candidate_detail_3(request):
    return render(request, 'pages/candidate-detail-3.html')

def advance_search(request):
    return render(request, 'pages/advance-search.html')

def candidate_dashboard(request):
    return render(request, 'pages/candidate-dashboard.html')

def candidate_profile(request):
    # Redirect to the profile detail for the current authenticated user
    if request.user.is_authenticated:
        return redirect('App:candidate_profile_detail', username=request.user.username)
    # If not authenticated, send them to the home page
    return redirect('App:index')


def candidate_profile_detail(request, username):
    # Show the profile for the given username
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.filter(user=user).first()
    return render(request, 'pages/candidate-profile.html', {'profile_user': user, 'profile': profile})


def is_rpo_admin(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    profile = Profile.objects.filter(user=user).first()
    return bool(profile and profile.role == 'rpo_admin')


def assign_roles(request):
    # Only RPO Admins (or superusers) can access
    if not is_rpo_admin(request.user):
        return HttpResponseForbidden('Forbidden')

    if request.method == 'POST':
        form = RoleAssignForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            role = form.cleaned_data['role']
            user = get_object_or_404(User, username=username)
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()
            messages.success(request, f"Updated role for {username} to {dict(Profile.ROLE_CHOICES).get(role)}")
            return redirect('App:assign_roles')
    else:
        form = RoleAssignForm()

    users = User.objects.order_by('username').all()
    profiles = {p.user_id: p for p in Profile.objects.filter(user__in=users)}

    # prepare small list of (user, profile, form) tuples
    user_rows = []
    for u in users:
        p = profiles.get(u.id)
        initial = {'username': u.username, 'role': p.role if p else 'candidate'}
        frm = RoleAssignForm(initial=initial)
        user_rows.append((u, p, frm))

    return render(request, 'pages/assign-roles.html', {'user_rows': user_rows, 'form': form})


def assign_role_ajax(request):
    # JSON endpoint to update a user's role via AJAX
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if not is_rpo_admin(request.user):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    username = request.POST.get('username')
    role = request.POST.get('role')
    if not username or not role:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    # Validate role
    valid_roles = [r[0] for r in Profile.ROLE_CHOICES]
    if role not in valid_roles:
        return JsonResponse({'error': 'Invalid role'}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    profile, _ = Profile.objects.get_or_create(user=user)
    profile.role = role
    profile.save()

    return JsonResponse({'ok': True, 'username': username, 'role': profile.role})

def candidate_resume(request):
    return render(request, 'pages/candidate-resume.html')

def candidate_applied_jobs(request):
    return render(request, 'pages/candidate-applied-jobs.html')

def candidate_alert_job(request):
    return render(request, 'pages/candidate-alert-job.html')

def candidate_saved_jobs(request):
    return render(request, 'pages/candidate-saved-jobs.html')

def candidate_follow_employers(request):
    return render(request, 'pages/candidate-follow-employers.html')

def candidate_messages(request):
    return render(request, 'pages/candidate-messages.html')

def candidate_change_password(request):
    return render(request, 'pages/candidate-change-password.html')

def candidate_delete_account(request):
    return render(request, 'pages/candidate-delete-account.html')

def employer_grid_1(request):
    return render(request, 'pages/employer-grid-1.html')

def employer_grid_2(request):
    return render(request, 'pages/employer-grid-2.html')

def employer_list_1(request):
    return render(request, 'pages/employer-list-1.html')

def employer_half_map(request):
    return render(request, 'pages/employer-half-map.html')

def employer_half_map_list(request):
    return render(request, 'pages/employer-half-map-list.html')

def employer_list_or_default(request):
    # Get employers from the database
    employers = Employer.objects.all()  # or any filter you need
    return render(request,'pages/employer-detail.html', {'employers': employers})

def employer_detail(request, title):
    employer = get_object_or_404(Employer, slug=title)  # Match the employer by title (or slug, depending on how your model is set up)
    return render(request, 'pages/employer-detail.html', {'employer': employer})

def employer_detail_2(request):
    return render(request, 'pages/employer-detail-2.html')

def employer_dashboard(request):
    return render(request, 'pages/employer-dashboard.html')

def employer_profile(request):
    return render(request, 'pages/employer-profile.html')

def employer_jobs(request):
    return render(request, 'pages/employer-jobs.html')

def employer_submit_job(request):
    return render(request, 'pages/employer-submit-job.html')

def employer_applicants_jobs(request):
    return render(request, 'pages/employer-applicants-jobs.html')

def employer_shortlist_candidates(request):
    return render(request, 'pages/employer-shortlist-candidates.html')

def employer_package(request):
    return render(request, 'pages/employer-package.html')

def employer_messages(request):
    return render(request, 'pages/employer-messages.html')

def employer_change_password(request):
    return render(request, 'pages/employer-change-password.html')

def employer_delete_account(request):
    return render(request, 'pages/employer-delete-account.html')

def about_us(request):
    return render(request, 'pages/about-us.html')

def notFound(request):
    return render(request, 'pages/404.html')

def checkout(request):
    return render(request, 'pages/checkout.html')

def blog(request):
    return render(request, 'pages/blog.html')

def blog_list_or_default(request):
    # Get blogs from the database
    blogs = Blog.objects.all()  # or any filter you need
    return render(request,'pages/blog-detail.html', {'blogs': blogs})

def blog_detail(request, title):
    blog = get_object_or_404(Blog, slug=title)  # Match the blog by title (or slug, depending on how your model is set up)
    return render(request, 'pages/blog-detail.html', {'blog': blog})

def privacy(request):
    return render(request, 'pages/privacy.html')

def pricing(request):
    return render(request, 'pages/pricing.html')

def faq(request):
    return render(request, 'pages/faq.html')

def contact(request):
    return render(request, 'pages/contact.html')

def help(request):
    return render(request, 'pages/help.html')

def job_list_or_default(request):
    # Get jobs from the database
    jobs = Job.objects.all()  # or any filter you need
    return render(request,'pages/job-detail.html', {'jobs': jobs})

def job_detail(request, title):
    job = get_object_or_404(Job, slug=title)  # Match the job by title (or slug, depending on how your model is set up)
    return render(request, 'pages/job-detail.html', {'job': job})

def signup(request):
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

def slider_home(request):
    return render(request, 'pages/slider-home.html')


def login_view(request):
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
            # Append ?login=failed so frontend can detect and open modal
            if '?' in next_url:
                return redirect(f"{next_url}&login=failed")
            return redirect(f"{next_url}?login=failed")
    # For GET or other, just redirect to index
    return redirect('App:index')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('App:index')