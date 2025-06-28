from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from datetime import datetime
from dateutil.parser import parse
from django.contrib import messages
from django.core.management import call_command
from mainapp.utils.anime_scraper import update_anime_data

from .models import (
    HololiveChannel, NijisanjiChannel, AogiriChannel,
    MilprChannel, SelfChannel, VsingerChannel, AnimeCard, Manga
)
from mainapp.utils.youtube_utils import update_channel_info
from .utils.manga_scraper import update_manga_data


import requests
from bs4 import BeautifulSoup

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


# 頁面：首頁、漫畫、小說
def index(request):
    return render(request, 'mainapp/index.html')

def anime(request):
    anime_list = AnimeCard.objects.all().order_by('-last_updated')
    return render(request, "mainapp/anime.html", {"anime_list": anime_list})


def manga(request):
    manga_data = Manga.objects.all().order_by('-update_time')
    return render(request, "mainapp/manga.html", {"manga_data": manga_data})

def novel(request):
    return render(request, 'mainapp/novel.html')


# 分類對應模型
MODEL_MAP = {
    "hololive": HololiveChannel,
    "nijisanji": NijisanjiChannel,
    "aogiri": AogiriChannel,
    "milpr": MilprChannel,
    "self": SelfChannel,
    "singer": VsingerChannel,
}



def frontend_update_group(request, group):
    if request.method == "POST":
        Model = MODEL_MAP.get(group.lower())
        if not Model:
            messages.error(request, "找不到對應的資料表")
            return redirect(f"/stream/{group}")

        all_channels = Model.objects.all()
        updated_count = 0
        
        for obj in all_channels:
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

                obj.last_updated = datetime.now()  # ✅ 寫入最後更新時間
                obj.save()
                updated_count += 1
            except Exception as e:
                print(f"更新 {obj.name} 失敗：{e}")

        messages.success(request, f"✅ {group} 頁面資料已更新，共 {updated_count} 筆")
        return redirect(f"/stream/{group}")



# 頁面：直播卡片顯示
def stream(request, group):
    selected = request.GET.get("group", "")
    Model = MODEL_MAP.get(group)
    if not Model:
        return render(request, 'mainapp/stream.html', {'error': '無效的 group'})

    groups = Model.objects.values_list("group_name", flat=True).distinct()
    rows = Model.objects.filter(group_name=selected) if selected else Model.objects.all()
    latest_update = rows.order_by("-last_updated").first().last_updated if rows else None
    now = datetime.now()
    cards = []

    for row in rows:
        try:
            dt_start = parse(row.live_start_time) if row.live_start_time else None
            live = {
                'title': row.live_title,
                'url': row.live_url,
                'thumbnail': row.live_thumbnail,
                'start_time': dt_start.strftime("%Y-%m-%d %H:%M") if dt_start and row.live_url else ''
            } if dt_start and row.live_url and dt_start > now else {
                'title': '目前沒有規劃',
                'url': '',
                'thumbnail': '',
                'start_time': ''
            }

            video = {
                'title': row.latest_video_title,
                'url': row.latest_video_url,
                'thumbnail': row.latest_video_thumbnail,
                'duration': row.latest_video_duration,
                'view_count': row.latest_video_views,
                'published_at': row.latest_video_published
            }

            cards.append({
                'name': row.name,
                'url': row.channel_url,
                'info': {
                    'channel_title': row.name,
                    'channel_avatar': row.channel_avatar,
                    'latest_video': video,
                    'live': live
                }
            })

        except Exception as e:
            print(f"錯誤處理資料 {row.name}: {e}")

    return render(request, 'mainapp/stream.html', {
        'table': group,
        'groups': groups,
        'selected_group': selected,
        'cards': cards,
        'now': now,
        'latest_update': latest_update
    })


def frontend_update_anime(request):
    if request.method == "POST":
        call_command("fetch_anime_data")
        messages.success(request, "✅ 動畫資料已更新")
    return redirect("anime")


def update_manga(request):
    update_manga_data()
    return redirect("manga")

def refresh_anime(request):
    update_anime_data()
    return JsonResponse({"status": "success", "message": "已更新動畫資料"})



import base64
import io
from PIL import Image, ImageOps
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings



# 載入你的模型（只需執行一次）
#from tensorflow.keras.models import load_model
#MODEL_PATH = os.path.join(settings.BASE_DIR, 'mainapp', 'model', 'mnist_model.h5')
#model = load_model(MODEL_PATH)

@csrf_exempt
def predict_digit(request):
    import json
    if request.method == 'POST':
        data = json.loads(request.body)
        img_str = data['image'].split(',')[1]
        img_bytes = base64.b64decode(img_str)
        img = Image.open(io.BytesIO(img_bytes)).convert('L')  # 灰階
        img = ImageOps.invert(img)
        img = img.resize((28, 28))
        img_np = np.array(img) / 255.0
        img_np = img_np.reshape(1, 28, 28, 1)
        pred = model.predict(img_np)
        result = int(np.argmax(pred))
        img.save('debug_upload.png')
        return JsonResponse({'result': result})
