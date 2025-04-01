# Generated by Django 5.1.3 on 2025-03-30 12:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentRegistration', '0002_registrationwindow_end_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentregistration',
            name='minor_subjects_chosen',
        ),
        migrations.RemoveField(
            model_name='studentregistration',
            name='officer_notes',
        ),
        migrations.RemoveField(
            model_name='studentregistration',
            name='preferred_class_time',
        ),
        migrations.AddField(
            model_name='studentregistration',
            name='preferred_class_days',
            field=models.CharField(blank=True, help_text='Comma-separated list of preferred class days (e.g., Monday,Thursday,Saturday)', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='studentregistration',
            name='preferred_time_end',
            field=models.TimeField(default=django.utils.timezone.now, help_text='Preferred end time for classes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentregistration',
            name='preferred_time_start',
            field=models.TimeField(default=django.utils.timezone.now, help_text='Preferred start time for classes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentregistration',
            name='selected_minor_subjects',
            field=models.CharField(blank=True, help_text='Comma-separated list of selected minor subject IDs', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='studentregistration',
            name='submitted',
            field=models.BooleanField(default=False, help_text='Indicates if the registration form has been submitted by the student'),
        ),
        migrations.AlterField(
            model_name='studentregistration',
            name='preferred_section',
            field=models.CharField(choices=[('Section A', 'Section A'), ('Section B', 'Section B'), ('Section C', 'Section C')], default='Section A', help_text="Student's preferred section", max_length=20),
        ),
        migrations.AlterField(
            model_name='studentregistration',
            name='registration_form_image',
            field=models.ImageField(blank=True, help_text='Final registration form image uploaded by the officer', null=True, upload_to='registration_forms/'),
        ),
    ]
