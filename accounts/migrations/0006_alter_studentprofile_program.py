# Generated by Django 5.1.4 on 2025-03-12 06:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_program'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='program',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.program'),
        ),
    ]
