import os
import logging
from pprint import pformat
from functools import cache
from googleapiclient.discovery import build
from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv()
load_dotenv()

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
logger = logging.getLogger(__name__)


def get_youtuber_statistics(youtuber_handle):
    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey=GOOGLE_API_KEY)
    request = youtube.channels().list(
        part="brandingSettings,contentDetails,contentOwnerDetails,id,localizations,snippet,statistics,status,"
             "topicDetails",
        forHandle=youtuber_handle
    )

    response = request.execute()
    return response


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

    video_categories = _get_video_categories()
    result['category'] = video_categories[result['categoryId']]
    return result


@cache  # we use this to save a bit on reruns of 'get_video_categories'.
def _get_video_categories():
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
    # video_id = "c8OwVTBdE6s"
    # logger.info(pformat(_get_video_categories()))
    # logger.info(pformat(get_video_statistics(video_id)))
    youtuber_handle = "@Coachella"
    logger.info(pformat(get_youtuber_statistics(youtuber_handle)))

