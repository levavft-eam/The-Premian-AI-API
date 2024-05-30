from yt_dlp import YoutubeDL  # type: ignore
from pathlib import Path

THIS_FOLDER = Path(__file__).parent.resolve()
DATA_DIR = THIS_FOLDER / '..' / '..' / 'data' / 'videos'


final_filename = None


def _yt_dlp_monitor(d):
    global final_filename
    final_filename = d.get('info_dict').get('_filename')


def download_video(video_id, archive=True):
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': f'{DATA_DIR}/%(id)s.%(ext)s',
        'progress_hooks': [_yt_dlp_monitor],
        # 'quiet': True,
        # 'no_warnings': True, 
        # 'postprocessors': [{
        #     'key': 'ExecAfterDownload',  # Execute a command after download
        #     'exec_cmd': 'ffmpeg -i {} -ss 00:00:00 -t 30 -c copy {}_trimmed.mp4',  # Trim the first 30 seconds
        # }],
    }
    if archive:
        ydl_opts['download_archive'] = 'download_archive.txt'

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    global final_filename
    if final_filename in {None, ""}:
        # TODO: search the data directory for files starting with {video_id} instead.
        final_filename = f"{video_id}.webm"
    return final_filename


def list_formats(video_id):
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'listformats': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([video_url])
    return result
