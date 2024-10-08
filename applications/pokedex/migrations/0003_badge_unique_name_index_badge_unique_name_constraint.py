# Generated by Django 5.0.7 on 2024-08-21 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0002_profile_unique_attendee_index_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='badge',
            index=models.Index(fields=['name'], name='unique_name_index'),
        ),
        migrations.AddConstraint(
            model_name='badge',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_name_constraint'),
        ),
    ]
