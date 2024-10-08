# Generated by Django 5.0.7 on 2024-08-15 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_registration_entry_hour_registration_exit_hour'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='slug',
            field=models.SlugField(max_length=500, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='is_confirmed',
            field=models.BooleanField(default=True),
        ),
    ]
