# Generated by Django 3.2.5 on 2021-08-13 05:06

import django.core.validators
from django.db import migrations, models
import video_to_audio.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to=video_to_audio.models.rename_and_save, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'mkv', 'mov', 'wmv', 'flv', 'avi', 'avchd', 'webm'])])),
            ],
        ),
    ]
