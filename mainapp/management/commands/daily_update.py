from django.core.management.base import BaseCommand
from mainapp.models import (
    HololiveChannel, NijisanjiChannel, AogiriChannel,
    SelfChannel, MilprChannel, VsingerChannel
)
from mainapp.utils.youtube_utils import update_channel_info, update_channel_cache


class Command(BaseCommand):
    help = "每日更新頻道快取資料"

    def handle(self, *args, **kwargs):
        table_map = {
            'hololive': HololiveChannel,
            'nijisanji': NijisanjiChannel,
            'aogiri': AogiriChannel,
            'self': SelfChannel,
            'milpr': MilprChannel,
            'singer': VsingerChannel
        }

        for name, model in table_map.items():
            self.stdout.write(self.style.NOTICE(f"🔁 正在更新 {name}..."))

            for channel in model.objects.all():
                self.stdout.write(f"  → 更新 {channel.name}...")

                try:
                    result = update_channel_info(channel.channel_url)
                    if result and 'error' not in result:
                        update_channel_cache(name, channel.name, result)
                        self.stdout.write(self.style.SUCCESS(f"    ✅ {channel.name} 更新成功"))
                    else:
                        self.stdout.write(self.style.WARNING(f"    ⚠️ {channel.name} 更新失敗"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"    ❌ 發生錯誤：{e}"))

        self.stdout.write(self.style.SUCCESS("🎉 所有頻道資料更新完畢"))
