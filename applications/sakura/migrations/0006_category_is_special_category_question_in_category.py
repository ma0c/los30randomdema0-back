# Generated by Django 5.0.7 on 2024-09-08 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sakura', '0005_category_front_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_special',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='question_in_category',
            field=models.IntegerField(default=5),
        ),
    ]
