from yt_dlp import YoutubeDL
import os

BASE_DIR = "../data"


final_filename = None


def _yt_dlp_monitor(d):
    global final_filename
    final_filename = d.get('info_dict').get('_filename')


def download_video(video_id):
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        # 'format': 'best[height<=720]',
        'format': 'bestaudio',
        'outtmpl': f'{BASE_DIR}/%(id)s.%(ext)s',
        'download_archive': 'download_archive.txt',
        'progress_hooks': [_yt_dlp_monitor]
        # 'postprocessors': [{
        #     'key': 'ExecAfterDownload',  # Execute a command after download
        #     'exec_cmd': 'ffmpeg -i {} -ss 00:00:00 -t 30 -c copy {}_trimmed.mp4',  # Trim the first 30 seconds
        # }],

    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return final_filename


def list_formats(video_id):
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'listformats': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([video_url])
    return result