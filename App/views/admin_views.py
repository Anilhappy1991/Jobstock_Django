"""
Admin/RPO views - Role assignment and management
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages

from App.models import Profile
from App.forms import RoleAssignForm


def is_rpo_admin(user):
    """Check if user is RPO admin"""
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    profile = Profile.objects.filter(user=user).first()
    return bool(profile and profile.role == 'rpo_admin')


def assign_roles(request):
    """Assign roles to users (RPO admin only)"""
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

    # Prepare list of (user, profile, form) tuples
    user_rows = []
    for u in users:
        p = profiles.get(u.id)
        initial = {'username': u.username, 'role': p.role if p else 'candidate'}
        frm = RoleAssignForm(initial=initial)
        user_rows.append((u, p, frm))

    return render(request, 'pages/assign-roles.html', {'user_rows': user_rows, 'form': form})


def assign_role_ajax(request):
    """JSON endpoint to update a user's role via AJAX"""
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
