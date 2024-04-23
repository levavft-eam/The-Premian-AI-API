import os
import logging
from pprint import pformat
from googleapiclient.discovery import build
from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv()
load_dotenv()

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
logger = logging.getLogger(__name__)


def get_video_statistics(video_id):
    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey=GOOGLE_API_KEY)
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )

    result = request.execute()

    result = result['items'][0]
    snippet = result['snippet']

    result = {
        'duration': result['contentDetails']['duration'],
        'id': result['id'],
        'statistics': result['statistics']
    }

    required_items = (
        'categoryId',
        'channelId',
        'channelTitle',
        'description',
        'publishedAt',
        'tags',
        'title',
        'thumbnails',
    )
    for item in required_items:
        result[item] = snippet[item]
    return result


def get_video_categories():
    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey=GOOGLE_API_KEY)
    request = youtube.videoCategories().list(
        part="snippet",
        hl="en_us",
        regionCode="KR"
    )

    result = request.execute()
    result = {item['id']: item['snippet']['title'] for item in result['items']}
    return result


def test():
    video_id = "c8OwVTBdE6s"
    logger.info(pformat(get_video_categories()))
    logger.info(pformat(get_video_statistics(video_id)))

