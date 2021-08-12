import os
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import *
import moviepy.editor as mp
from converter.settings import MEDIA_URL
from pytube import *


def get_audio(video_path, type, start, end):
    video = mp.VideoFileClip(video_path).subclip(start, end)
    audio_filename = video_path.split('/')[-1].split('.')[0] + f'.{ type }'
    response = HttpResponse(
        content_type=f'audio/{type}',
        headers={'Content-Disposition': f'attachment; filename="converted.{type}"'},
    )
    video.audio.write_audiofile(audio_filename)
    response.write(open(audio_filename, 'rb').read())
    if os.path.exists(audio_filename):
        os.remove(audio_filename)
    return response


def from_youtube(request):
    if request.method == "POST":
        video = YouTube(request.POST.get('url'))
        os.chdir('media/videos')
        video_path = video.streams.get_lowest_resolution().download()
        os.chdir('../..')
        video = VideoModel.objects.create(video=video_path.split('media/')[-1])
        return redirect('video', video_id=video.id)
    context = {
        'upload': 'from-youtube',
    }
    return render(request, 'videos/index.html', context)


# Create your views here.
def upload_video(request):
    form = VideoForm()
    message = ''
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            return redirect('video', video_id=video.id)
        else:
            message = 'Not valid!!!'
    
    context = {
        'form': form,
        'message': message,
    }

    return render(request, 'videos/index.html', context)


def video_show(request, video_id):
    try:
        video = VideoModel.objects.get(id=video_id)
        video_filename = str(video.video).split('/')[-1]
        video_path = f'media/videos/{video_filename}'
    except Exception:
        return redirect('upload')

    if request.method == "POST":
        if request.POST.get('to-audio'):
            start_time = int(request.POST.get('start')) if request.POST.get('start') else 0
            end_time = request.POST.get('end')
            video = mp.VideoFileClip(video_path)
            if not end_time or int(end_time) > video.duration:
                end_time = video.duration
            if start_time > int(end_time):
                start_time = 0
            return get_audio(video_path, request.POST.get('to-audio'), start_time, end_time)

    context = {
        'video': video,
        'MEDIA_URL': MEDIA_URL,
    }
    return render(request, 'videos/video.html', context)
