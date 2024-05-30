import os
import json
import logging
from pprint import pformat
from functools import cache
from googleapiclient.discovery import build # type: ignore
from dotenv import find_dotenv, load_dotenv # type: ignore

env_file = find_dotenv()
load_dotenv()

logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=GOOGLE_API_KEY)


def get_playlist_items(playlist_id):
    next_page_token = None
    results = []
    while True:
        results.append(youtube.playlistItems().list(
            part="snippet,contentDetails,id",
            playlistId=playlist_id,
            pageToken=next_page_token,
        ).execute())

        next_page_token = results[-1].get('nextPageToken')

        if next_page_token is None:
            break

    return [item for r in results for item in r['items']]


def get_channel_playlists(channel_id):
    next_page_token = None
    results = []
    while True:
        results.append(youtube.playlists().list(
            part="contentDetails, id, snippet",
            channelId=channel_id,
            pageToken=next_page_token,
            # maxResults=30
        ).execute())

        next_page_token = results[-1].get('nextPageToken')

        if next_page_token is None:
            break

    return [item for r in results for item in r['items']]


# prob useless
def get_channel_sections(channel_id):
    return youtube.channelSections().list(
        part="id,snippet, contentDetails",
        channelId=channel_id
    ).execute()


def get_channel_details(channel_handle=None, channel_id=None, n=5):
    statistics = get_channel_statistics(channel_handle, channel_id)[0]
    channel_id = statistics["id"]
    channel_handle = statistics["snippet"]["customUrl"]
    videos = search_recent_n_videos(channel_id, channel_handle, n)
    result = {
        "channel": {
            "country": statistics["brandingSettings"]["channel"]["country"],
            "description": statistics["brandingSettings"]["channel"]["description"],
            "title": statistics["brandingSettings"]["channel"]["title"],
        },
        "custom_url": statistics["snippet"]["customUrl"],
        "published_at": statistics["snippet"]["publishedAt"],
        "thumbnail_url": statistics["snippet"]["thumbnails"]["default"]["url"],
        "statistics": statistics["statistics"],
        "channel_id": channel_id,
        "channel_handle": channel_handle,
        "videos": []
    }
    for video in videos["items"]:
        video_id = video["id"]["videoId"]
        kind = video["id"]["kind"]
        video_channel_id = video["snippet"]["channelId"]
        if video_channel_id != channel_id or kind != "youtube#video":
            continue
        result["videos"].append({
            "video_id": video_id,
            "snippet": video["snippet"]
        })

    return result


def get_channel_statistics(channel_handle=None, channel_id=None):
    if channel_handle is channel_id is None:
        raise Exception(f"get_channel_statistics requires one of channel_handle and channel_id to be set but: {channel_handle=}, {channel_id=}")
    
    request = youtube.channels().list(
        part="brandingSettings,contentDetails,contentOwnerDetails,id,localizations,snippet,statistics,status,"
             "topicDetails",
        forHandle=channel_handle,
        id=channel_id
    )

    return request.execute()


def search_recent_n_videos(channel_id, channel_handle, n=5):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=n,
        order="date",
        q=channel_handle,
        type="video"
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
        result[item] = snippet.get(item)

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
    # logger.info(pformat(get_channel_statistics(channel_handle)))

    # channel_id = "UCHF66aWLOxBW4l6VkSrS3cQ"
    # logger.info(json.dumps(get_channel_playlists(channel_id), ensure_ascii=False))  # https://jsonviewer.stack.hu/

    playlist_id = "PLIjqRbAQP0WK7RdK-yzcfVmE3k_O5Xpff"
    logger.info(json.dumps(get_playlist_items(playlist_id), ensure_ascii=False))  # https://jsonviewer.stack.hu/


