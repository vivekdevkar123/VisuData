# Generated by Django 3.2.12 on 2023-07-29 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('dataset_id', models.AutoField(primary_key=True, serialize=False)),
                ('dataset_name', models.CharField(max_length=100)),
                ('uploaded_file', models.FileField(upload_to='datasets/')),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
