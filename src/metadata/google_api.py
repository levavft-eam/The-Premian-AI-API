import os
from googleapiclient.discovery import build
from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv()
load_dotenv()

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]


def get_video_statistics(video_id):
    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey=GOOGLE_API_KEY)
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    return request.execute()


def get_video_categories():
    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey=GOOGLE_API_KEY)
    request = youtube.videoCategories().list(
        part="snippet",
        hl="en_us",
        regionCode="KR"
    )
    return request.execute()
