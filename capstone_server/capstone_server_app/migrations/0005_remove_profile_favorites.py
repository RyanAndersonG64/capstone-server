# Generated by Django 5.0.6 on 2024-06-12 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capstone_server_app', '0004_profile_favorites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='favorites',
        ),
    ]
