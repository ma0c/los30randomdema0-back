# Generated by Django 5.0.7 on 2024-08-11 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_possibleattendees_unique_name_phone_index_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='entry_hour',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='exit_hour',
            field=models.DateTimeField(null=True),
        ),
    ]
