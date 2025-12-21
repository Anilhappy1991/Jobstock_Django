from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Reset passwords for all users to H@ppy123'

    def handle(self, *args, **options):
        new_password = 'H@ppy123'
        
        # List of usernames to update
        usernames = ['hiring_manager', 'rpo_admin', 'system_admin', 'rituranjangupta']
        
        updated_count = 0
        for username in usernames:
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated password for user: {username}')
                )
                updated_count += 1
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'User not found: {username}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nTotal users updated: {updated_count}')
        )
