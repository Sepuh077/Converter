from django.urls import path
from .views import *


urlpatterns = [
    path('upload/', upload_video, name='upload'),
    path('from-youtube/', from_youtube, name='youtube'),
    path('upload/<str:video_id>/', video_show, name='video'),
    path('from_youtube/<str:url>/', video_show_from_youtube, name='youtube_video'),
]
