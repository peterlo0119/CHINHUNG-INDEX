import itertools
from datetime import datetime, timedelta
from googleapiclient.discovery import build
import isodate

# 你的 YouTube API 金鑰（循環使用）
API_KEYS = [
    "AIzaSyD9YsIVc2uQW8WyWGBUpkYOhiwSMSNYOEI",
    "AIzaSyDM5VMwanVK3cGtRgYIWwQbwAXC-NzEG8w",
    "AIzaSyDM5VMwanVK3cGtRgYIWwQbwAXC-NzEG8w",
    "AIzaSyChEWT7wXVk3yEMqldG4KH6xBcHmS1EuoY",
    "AIzaSyCYqXB2CrbRRx8MgflKHd66NjnoRy61UEo",
    "AIzaSyAWL77gu2PNogdEJhsigY6Y2--UBzxgKNs"
]
api_key_cycle = itertools.cycle(API_KEYS)


def get_youtube_client():
    key = next(api_key_cycle)
    return build("youtube", "v3", developerKey=key)


def extract_channel_id(url):
    if "/channel/" in url:
        return url.split("/channel/")[-1].split("/")[0]
    elif "@" in url:
        return None
    return None


def update_channel_info(channel_url):
    channel_id = extract_channel_id(channel_url)
    if not channel_id:
        raise ValueError("無法解析 Channel ID")

    youtube = get_youtube_client()

    # 抓頻道基本資料
    channel_info = youtube.channels().list(
        part="snippet,contentDetails",
        id=channel_id
    ).execute()

    if not channel_info['items']:
        raise ValueError("找不到頻道")

    channel = channel_info['items'][0]
    channel_title = channel['snippet']['title']
    channel_avatar = channel['snippet']['thumbnails']['high']['url']
    upload_playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']

    # 抓即將開始的直播（若有）
    search_live = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        eventType="upcoming",
        type="video",
        order="date",
        maxResults=1
    ).execute()

    live_info = None
    if search_live['items']:
        live = search_live['items'][0]
        video_id = live['id']['videoId']
        video_data = youtube.videos().list(
            part="liveStreamingDetails",
            id=video_id
        ).execute()

        scheduled_utc_str = video_data['items'][0]['liveStreamingDetails'].get('scheduledStartTime')
        if scheduled_utc_str:
            scheduled_utc = datetime.strptime(scheduled_utc_str, "%Y-%m-%dT%H:%M:%SZ")
            scheduled_tw = scheduled_utc + timedelta(hours=8)
            formatted_time = scheduled_tw.strftime("%Y-%m-%d %H:%M")
        else:
            formatted_time = "無直播時間"

        live_info = {
            'title': live['snippet']['title'],
            'thumbnail': live['snippet']['thumbnails']['high']['url'],
            'url': f"https://www.youtube.com/watch?v={video_id}",
            'start_time': formatted_time
        }

    # 抓最新影片（不含尚未開播的直播）
    uploads = youtube.playlistItems().list(
        part="snippet",
        playlistId=upload_playlist_id,
        maxResults=5
    ).execute()

    latest_video_id = None
    for item in uploads["items"]:
        video_id = item["snippet"]["resourceId"]["videoId"]
        video_info = youtube.videos().list(
            part="snippet,contentDetails,liveStreamingDetails,statistics",
            id=video_id
        ).execute()
        video = video_info["items"][0]

        if "liveStreamingDetails" in video and "actualStartTime" not in video["liveStreamingDetails"]:
            continue  # 尚未開播的不當作影片
        latest_video_id = video_id
        break

    if not latest_video_id:
        raise ValueError("沒有有效影片")

    # 撈影片詳細資訊
    video_info = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=latest_video_id
    ).execute()

    video = video_info["items"][0]
    video_data = {
        'title': video["snippet"]["title"],
        'thumbnail': video["snippet"]["thumbnails"]["high"]["url"],
        'url': f"https://www.youtube.com/watch?v={latest_video_id}",
        'duration': isodate.parse_duration(video["contentDetails"]["duration"]),
        'view_count': video["statistics"].get("viewCount", "N/A"),
        'published_at': video["snippet"]["publishedAt"]
    }

    return {
        'channel_title': channel_title,
        'channel_avatar': channel_avatar,
        'live': live_info,
        'latest_video': video_data
    }
