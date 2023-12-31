# Generated by Django 4.2.3 on 2023-08-12 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('EDA', '0004_note_heading'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('plot_id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.JSONField()),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EDA.dataset')),
            ],
        ),
    ]
