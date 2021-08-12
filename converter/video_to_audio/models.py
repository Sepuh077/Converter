from django.db import models
import os
from django.core.validators import FileExtensionValidator


VIDEO_FORMATS = [
    'mp4',
    'mkv',
    'mov',
    'wmv',
    'flv',
    'avi',
    'avchd',
    'webm',
]


def rename_and_save(instance, filename):
    upload_to='videos'
    ext = filename.split('.')[-1]

    try:
        filename = f'{VideoModel.objects.last().id + 1}.{ext}'
    except Exception:
        filename = f'1.{ext}'

    return os.path.join(upload_to, filename)


# Create your models here.
class VideoModel(models.Model):
    video = models.FileField(
        upload_to=rename_and_save, 
        validators=[FileExtensionValidator(allowed_extensions=VIDEO_FORMATS)]
    )
