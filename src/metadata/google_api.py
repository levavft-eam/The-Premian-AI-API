import os
import logging
from pprint import pformat
from functools import cache
from googleapiclient.discovery import build
from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv()
load_dotenv()

logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=GOOGLE_API_KEY)


def get_playlist_items(playlist_id):
    return youtube.playlistItems().list(
        part="snippet,contentDetails,id",
        playlistId=playlist_id
    ).execute()


def get_channel_playlists(channel_id):
    return youtube.playlists().list(
        part="contentDetails, id, snippet",
        channelId=channel_id,
        # maxResults=30
    ).execute()


# prob useless
def get_channel_sections(channel_id):
    return youtube.channelSections().list(
        part="id,snippet, contentDetails",
        channelId=channel_id
    ).execute()


def get_channel_statistics(channel_handle):
    request = youtube.channels().list(
        part="brandingSettings,contentDetails,contentOwnerDetails,id,localizations,snippet,statistics,status,"
             "topicDetails",
        forHandle=channel_handle
    )

    return request.execute()


def get_video_statistics(video_id):
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

    # channel_handle = "@Coachella"
    # logger.info(pformat(get_youtuber_statistics(channel_handle)))

    # channel_id = "UCHF66aWLOxBW4l6VkSrS3cQ"
    # logger.info(pformat(get_channel_sections(channel_id)))
    # logger.info(pformat(get_channel_playlists(channel_id)))

    playlist_id = "PLIjqRbAQP0WI1kdiUTD8btfDOGMSZ950U"
    logger.info(pformat(get_playlist_items(playlist_id)))


