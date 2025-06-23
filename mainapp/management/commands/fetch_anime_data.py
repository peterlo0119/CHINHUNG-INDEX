from django.core.management.base import BaseCommand
from mainapp.utils.anime_scraper import update_anime_data

class Command(BaseCommand):
    help = "爬取動畫資料並更新 AnimeCard"

    def handle(self, *args, **kwargs):
        try:
            update_anime_data()
            self.stdout.write(self.style.SUCCESS("✅ AnimeCard 已成功更新"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ 發生錯誤: {e}"))
