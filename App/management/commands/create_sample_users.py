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

        self.stdout.write(self.style.SUCCESS('Sample users created/updated.'))
