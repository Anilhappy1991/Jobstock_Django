# Generated migration to add role to Profile
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('rpo_admin', 'RPO Admin'), ('hiring_manager', 'Hiring Manager'), ('candidate', 'Candidate')], default='candidate', max_length=20),
        ),
    ]
