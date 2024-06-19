from yt_dlp import YoutubeDL, download_range_func  # type: ignore
from pathlib import Path

THIS_FOLDER = Path(__file__).parent.resolve()
DATA_DIR = THIS_FOLDER / '..' / '..' / 'data' / 'videos'


final_filename = None


def _yt_dlp_monitor(d):
    global final_filename
    final_filename = d.get('info_dict').get('_filename')

def _download_video(video_url, file_name, archive):
    start, end = 0, 60*20  # Start and end time in seconds.
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': f'{DATA_DIR}/%(id)s.%(ext)s',
        'progress_hooks': [_yt_dlp_monitor],
        'download_ranges': download_range_func(None, [(start, end)]), 
        'force_keyframes_at_cuts': True,
        # 'quiet': True,
        # 'no_warnings': True, 
    }
    if archive:
        ydl_opts['download_archive'] = 'download_archive.txt'

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    global final_filename
    if final_filename in {None, ""}:
        # TODO: search the data directory for files starting with {file_name} instead.
        final_filename = f"{file_name}.webm"
    return final_filename

def download_video(video_id, archive=True):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    file_name = video_id
    return _download_video(video_url, file_name, archive)


def list_formats(video_id):
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'listformats': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([video_url])
    return result
