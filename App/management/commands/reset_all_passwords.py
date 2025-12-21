"""
Management command to reset all user passwords to H@ppy123
Usage: python manage.py reset_all_passwords
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Reset all user passwords to H@ppy123'

    def handle(self, *args, **options):
        password = 'H@ppy123'
        users = User.objects.all()
        
        self.stdout.write(self.style.SUCCESS(f'Resetting passwords for {users.count()} users...'))
        
        for user in users:
            user.set_password(password)
            user.save()
            self.stdout.write(f'  ✓ Reset password for: {user.username}')
        
        self.stdout.write(self.style.SUCCESS('\nAll passwords have been reset to: H@ppy123'))
        self.stdout.write('You can now login with any username and password: H@ppy123')
