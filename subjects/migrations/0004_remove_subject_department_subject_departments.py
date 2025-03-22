# Generated by Django 5.1.4 on 2025-03-22 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('subjects', '0003_subject_semester'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='department',
        ),
        migrations.AddField(
            model_name='subject',
            name='departments',
            field=models.ManyToManyField(help_text='Select departments for which this subject is offered', related_name='subjects', to='accounts.department'),
        ),
    ]
