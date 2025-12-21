# Generated manually on 2025-12-21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0012_groupprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumeprocessing',
            name='error_details',
            field=models.JSONField(blank=True, help_text='Detailed error information including traceback and context', null=True),
        ),
    ]
