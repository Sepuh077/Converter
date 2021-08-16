import os
from django.http.response import HttpResponse
from .forms import *
import moviepy.editor as mp


def download_audio_from_youtube(audio):
    response = HttpResponse(
        content_type=f'audio/mp3',
        headers={'Content-Disposition': f'attachment; filename="converted.mp3"'},
    )
    audio.stream_to_buffer(response)
    return response


def download_video_from_youtube(video):
    response = HttpResponse(
        content_type=f'video/mp4',
        headers={'Content-Disposition': f'attachment; filename="converted.mp4"'},
    )
    video.stream_to_buffer(response)
    return response


def download_audio(video_path, type, start, end):
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


def config_timers(request, duration):
    start_time = int(request.POST.get('start')) if request.POST.get('start') else 0
    end_time = request.POST.get('end')
    if not end_time or int(end_time) > duration:
        end_time = duration
    if start_time > int(end_time):
        start_time = 0
    
    return start_time, end_time