# Generated by Django 5.0.6 on 2024-06-17 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capstone_server_app', '0011_profile_profileviewstate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profileViewState',
            new_name='profile_view_state',
        ),
    ]
