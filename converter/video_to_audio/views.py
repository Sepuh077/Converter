import os
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import *
import moviepy.editor as mp
from converter.settings import MEDIA_URL
from pytube import YouTube, exceptions
from pathlib import Path
from .helper import *


def from_youtube(request):
    message = ''
    if request.method == "POST":
        Path('media/videos').mkdir(exist_ok=True, parents=True)
        os.chdir('media/videos')
        try:
            url = request.POST.get('url')
            YouTube(url)
            return redirect('youtube_video', video_id=url.split('/')[-1])
        except exceptions.RegexMatchError:
            message = 'Type valid video url!'
    context = {
        'upload': 'from-youtube',
        'message': message,
    }
    return render(request, 'videos/index.html', context)


def upload_video(request):
    form = VideoForm()
    message = ''
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            return redirect('video', video_id=video.id)
        else:
            message = 'Choose video type object!'
    
    context = {
        'form': form,
        'message': message,
    }

    return render(request, 'videos/index.html', context)


def video_show_from_youtube(request, url):
    video = YouTube(url)
    if request.method == "POST":
        if request.POST.get('to-audio'):
            audio = video.streams.filter(only_audio=True).first()
            return download_audio_from_youtube(audio)
        elif request.POST.get('to-video'):
            video_file = video.streams.get_highest_resolution()
            return download_video_from_youtube(video_file)
    
    context = {
        'url': url.split('/')[-1],
        'MEDIA_URL': MEDIA_URL,
    }
    return render(request, 'videos/youtube.html', context)


def video_show(request, video_id):
    # try:
    try:
        video = VideoModel.objects.get(id=video_id)
        video_filename = str(video.video).split('/')[-1]
        video_path = f'media/videos/{video_filename}'
    except Exception:
        return video_show_from_youtube(request, f'https://youtu.be/{video_id}')
    # except Exception:
    #     return redirect('upload')

    if request.method == "POST":
        if request.POST.get('to-audio'):
            video = mp.VideoFileClip(video_path)
            start_time, end_time = config_timers(request, video.duration)
            return download_audio(video_path, request.POST.get('to-audio'), start_time, end_time)

    context = {
        'video': video,
        'MEDIA_URL': MEDIA_URL,
    }
    return render(request, 'videos/video.html', context)
