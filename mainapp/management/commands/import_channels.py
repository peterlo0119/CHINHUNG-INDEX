from django.core.management.base import BaseCommand
from mainapp.models import HololiveChannel
from mainapp.youtube_utils import get_channel_info  # 自訂的函式

class Command(BaseCommand):
    help = '更新 Hololive 頻道資料'

    def handle(self, *args, **kwargs):
        for ch in HololiveChannel.objects.all():
            print(f"🔄 正在更新：{ch.name}")
            data = get_channel_info(ch.channel_url)
            if "error" in data:
                print(f"❌ {ch.name} 失敗：{data['error']}")
                continue
            video = data["latest_video"]
            ch.latest_video_title = video["title"]
            ch.latest_video_url = video["url"]
            ch.latest_video_thumbnail = video["thumbnail"]
            ch.latest_video_duration = str(video["duration"])
            ch.latest_video_views = video["view_count"]
            ch.latest_video_published = video["published_at"]
            ch.channel_avatar = data["channel_avatar"]

            # 處理直播（有可能無）
            live = data.get("live")
            if live:
                ch.live_title = live["title"]
                ch.live_url = live["url"]
                ch.live_thumbnail = live["thumbnail"]
                ch.live_start_time = live["start_time"]
            else:
                ch.live_title = ch.live_url = ch.live_thumbnail = ch.live_start_time = None

            ch.save()
