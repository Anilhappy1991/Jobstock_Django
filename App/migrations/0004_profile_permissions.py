# Generated migration to add Profile permissions
from django.db import migrations


def create_permissions(apps, schema_editor):
    # Permissions will be created by Django automatically from model Meta, but
    # we include a no-op data migration to keep schema history consistent.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_profile_role'),
    ]

    operations = [
        migrations.RunPython(create_permissions, reverse_code=migrations.RunPython.noop),
    ]
