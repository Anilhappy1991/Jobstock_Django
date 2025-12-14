from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from App.models import Profile

User = get_user_model()

SAMPLE_USERS = [
    {
        'username': 'rpo_admin',
        'email': 'rpo_admin@example.com',
        'password': 'RpoAdminPass123!',
        'role': 'rpo_admin',
        'full_name': 'RPO Admin'
    },
    {
        'username': 'hiring_manager',
        'email': 'hiring_manager@example.com',
        'password': 'HiringMgrPass123!',
        'role': 'hiring_manager',
        'full_name': 'Hiring Manager'
    },
    {
        'username': 'candidate1',
        'email': 'candidate1@example.com',
        'password': 'CandidatePass123!',
        'role': 'candidate',
        'full_name': 'Sample Candidate'
    },
]


class Command(BaseCommand):
    help = 'Create sample users for RPO Admin, Hiring Manager, and Candidate'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Overwrite existing sample users')

    def handle(self, *args, **options):
        force = options['force']
        # Ensure groups and permissions exist
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType

        # Create groups
        groups = {
            'RPO Admin': {
                'perms': ['assign_roles', 'manage_platform']
            },
            'Hiring Manager': {
                'perms': ['review_candidates', 'add_job', 'change_job']
            },
            'Candidate': {
                'perms': ['apply_jobs']
            }
        }

        # Create groups and attach permissions
        for group_name, info in groups.items():
            grp, _ = Group.objects.get_or_create(name=group_name)
            for perm_codename in info['perms']:
                perm = Permission.objects.filter(codename=perm_codename).first()
                if not perm:
                    # try to create permission if missing
                    # first handle custom permissions attached to Profile model
                    ct_profile = ContentType.objects.get_for_model(Profile)
                    created = False
                    # Map known custom permission codenames to names
                    custom_map = {
                        'assign_roles': 'Can assign roles and manage user roles',
                        'manage_platform': 'Can manage platform settings and content',
                        'review_candidates': 'Can review and shortlist candidates',
                        'apply_jobs': 'Can apply to jobs'
                    }
                    if perm_codename in custom_map:
                        perm, created = Permission.objects.get_or_create(
                            codename=perm_codename,
                            content_type=ct_profile,
                            defaults={'name': custom_map[perm_codename]}
                        )
                    else:
                        # try interpret codename like add_model / change_model
                        parts = perm_codename.split('_', 1)
                        if len(parts) == 2:
                            action, model = parts
                            try:
                                ct = ContentType.objects.get(app_label='App', model=model)
                                name = f"Can {action} {model}"
                                perm, created = Permission.objects.get_or_create(codename=perm_codename, content_type=ct, defaults={'name': name})
                            except ContentType.DoesNotExist:
                                self.stdout.write(self.style.WARNING(f"ContentType for model {model} not found; permission {perm_codename} skipped"))
                        else:
                            self.stdout.write(self.style.WARNING(f"Permission {perm_codename} not found and cannot be created"))
                if perm:
                    grp.permissions.add(perm)
            grp.save()
        for u in SAMPLE_USERS:
            user, created = User.objects.get_or_create(username=u['username'], defaults={'email': u['email']})
            if created:
                user.set_password(u['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user {u['username']}"))
            else:
                if force:
                    user.email = u['email']
                    user.set_password(u['password'])
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f"Overwrote user {u['username']}"))
                else:
                    self.stdout.write(self.style.WARNING(f"User {u['username']} already exists; use --force to overwrite"))

            # ensure profile exists and set role/full_name
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = u['role']
            profile.full_name = u.get('full_name', profile.full_name)
            profile.save()

            # Add user to the appropriate group
            # Map role values to group names
            role_to_group = {
                'rpo_admin': 'RPO Admin',
                'hiring_manager': 'Hiring Manager',
                'candidate': 'Candidate',
            }
            grp_name = role_to_group.get(u['role'])
            if grp_name:
                grp = Group.objects.filter(name=grp_name).first()
                if grp:
                    user.groups.clear()
                    user.groups.add(grp)
                    user.save()
            profile.save()

        self.stdout.write(self.style.SUCCESS('Sample users created/updated.'))
