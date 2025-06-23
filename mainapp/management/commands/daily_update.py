from django.core.management.base import BaseCommand
from mainapp.views import get_db_connection, get_channel_info, update_channel_cache

class Command(BaseCommand):
    help = "每日更新頻道快取資料"

    def handle(self, *args, **kwargs):
        tables = ["hololive", "nijisanji", "aogiri", "self", "milpr", "singer"]
        for table in tables:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT name, channel_url FROM {table}")
            rows = cur.fetchall()
            conn.close()

            for row in rows:
                self.stdout.write(f"更新 {row['name']}...")
                result = get_channel_info(row["channel_url"])
                if result and 'error' not in result:
                    update_channel_cache(table, row["name"], result)
