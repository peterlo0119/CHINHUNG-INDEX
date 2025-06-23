from django.core.management.base import BaseCommand
from mainapp.models import (
    HololiveChannel, NijisanjiChannel, AogiriChannel,
    MilprChannel, SelfChannel, VsingerChannel
)
from mainapp.utils.youtube_utils import update_channel_info
from mainapp.utils.anime_scraper import update_anime_data
from mainapp.utils.manga_scraper import update_manga_data
from datetime import datetime

class Command(BaseCommand):
    help = "🧰 一鍵更新 YouTube 頻道 + 動畫 + 漫畫"

    def handle(self, *args, **options):
        # 更新 YouTube 所有 group
        MODEL_MAP = {
            "hololive": HololiveChannel,
            "nijisanji": NijisanjiChannel,
            "aogiri": AogiriChannel,
            "milpr": MilprChannel,
            "self": SelfChannel,
            "singer": VsingerChannel,
        }

        for name, Model in MODEL_MAP.items():
            self.stdout.write(f"🔄 更新 {name} 頻道...")
            updated_count = 0
            for obj in Model.objects.all():
                try:
                    info = update_channel_info(obj.channel_url)
                    obj.channel_avatar = info["channel_avatar"]
                    obj.latest_video_title = info["latest_video"]["title"]
                    obj.latest_video_url = info["latest_video"]["url"]
                    obj.latest_video_thumbnail = info["latest_video"]["thumbnail"]
                    obj.latest_video_duration = str(info["latest_video"]["duration"])
                    obj.latest_video_views = info["latest_video"]["view_count"]
                    obj.latest_video_published = info["latest_video"]["published_at"]

                    if info.get("live"):
                        obj.live_title = info["live"]["title"]
                        obj.live_url = info["live"]["url"]
                        obj.live_thumbnail = info["live"]["thumbnail"]
                        obj.live_start_time = info["live"]["start_time"]
                    else:
                        obj.live_title = obj.live_url = obj.live_thumbnail = obj.live_start_time = ""

                    obj.last_updated = datetime.now()
                    obj.save()
                    updated_count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"⚠️ {obj.name} 更新失敗: {e}"))
            self.stdout.write(self.style.SUCCESS(f"✅ {name} 共更新 {updated_count} 筆"))

        # 更新動畫
        self.stdout.write("🎬 更新動畫資料...")
        try:
            update_anime_data()
            self.stdout.write(self.style.SUCCESS("✅ 動畫更新完成"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ 動畫更新失敗: {e}"))

        # 更新漫畫
        self.stdout.write("📚 更新漫畫資料...")
        try:
            update_manga_data()
            self.stdout.write(self.style.SUCCESS("✅ 漫畫更新完成"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ 漫畫更新失敗: {e}"))
