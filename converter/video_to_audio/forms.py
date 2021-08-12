from typing import AbstractSet
from django import forms
from django.forms import fields, widgets
from .models import *


class VideoForm(forms.ModelForm):
    class Meta:
        model = VideoModel
        fields = [ 'video' ]
        widgets = {
            'video': forms.FileInput(
                attrs={
                    'style': '',
                    'value': 'Get',
                }
            )
        }
