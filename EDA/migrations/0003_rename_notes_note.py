# Generated by Django 4.2.3 on 2023-08-04 20:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EDA', '0002_notes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notes',
            new_name='Note',
        ),
    ]
