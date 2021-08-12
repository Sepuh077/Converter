from django.urls import path
from .views import video_show, upload_video, from_youtube


urlpatterns = [
    path('', upload_video, name='upload'),
    path('from-youtube/', from_youtube, name='youtube'),
    path('<str:video_id>/', video_show, name='video'),
]
