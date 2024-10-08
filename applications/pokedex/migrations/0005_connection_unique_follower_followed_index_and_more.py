# Generated by Django 5.0.7 on 2024-08-22 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0004_profile_number'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='connection',
            index=models.Index(fields=['follower', 'followed'], name='unique_follower_followed_index'),
        ),
        migrations.AddConstraint(
            model_name='connection',
            constraint=models.UniqueConstraint(fields=('follower', 'followed'), name='unique_follower_followed_constraint'),
        ),
    ]
