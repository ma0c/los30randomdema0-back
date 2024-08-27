# Generated by Django 5.0.7 on 2024-08-27 03:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('serial_number', models.IntegerField(unique=True)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('theme', models.CharField(max_length=255)),
                ('responsible', models.CharField(max_length=255)),
                ('evaluation_type', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ['serial_number'],
            },
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.UniqueConstraint(fields=('serial_number',), name='unique_question_serial_number'),
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.UniqueConstraint(fields=('slug',), name='unique_question_slug'),
        ),
    ]
