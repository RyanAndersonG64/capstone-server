# Generated by Django 5.0.6 on 2024-05-15 19:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cycling_store_app', '0006_alter_customerorder_created_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerorder',
            name='created_date',
            field=models.DateField(default=datetime.datetime(2024, 5, 15, 15, 13, 43, 74623)),
        ),
    ]
