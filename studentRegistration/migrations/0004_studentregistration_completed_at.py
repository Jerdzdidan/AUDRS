# Generated by Django 5.1.4 on 2025-04-14 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentRegistration', '0003_remove_studentregistration_minor_subjects_chosen_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentregistration',
            name='completed_at',
            field=models.DateTimeField(blank=True, help_text='Timestamp when the registration was completed', null=True),
        ),
    ]
