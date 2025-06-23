from django.db import models
from datetime import datetime

class BaseChannel(models.Model):
    name = models.CharField(max_length=100)
    channel_url = models.URLField()
    channel_avatar = models.URLField(blank=True, null=True)
    group_name = models.CharField(max_length=50, blank=True, null=True)

    latest_video_title = models.CharField(max_length=200, blank=True, null=True)
    latest_video_url = models.URLField(blank=True, null=True)
    latest_video_thumbnail = models.URLField(blank=True, null=True)
    latest_video_duration = models.CharField(max_length=20, blank=True, null=True)
    latest_video_views = models.CharField(max_length=20, blank=True, null=True)
    latest_video_published = models.CharField(max_length=50, blank=True, null=True)

    live_title = models.CharField(max_length=200, blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    live_thumbnail = models.URLField(blank=True, null=True)
    live_start_time = models.CharField(max_length=50, blank=True, null=True)

    # ✅ 建議補上 default=datetime.now，這樣一創建就會有時間
    last_updated = models.DateTimeField(default=datetime.now, blank=True, null=True)

    class Meta:
        abstract = True

class HololiveChannel(BaseChannel): pass
class NijisanjiChannel(BaseChannel): pass
class AogiriChannel(BaseChannel): pass
class MilprChannel(BaseChannel): pass
class SelfChannel(BaseChannel): pass
class VsingerChannel(BaseChannel): pass




class AnimeCard(models.Model):
    title = models.CharField(max_length=200)
    episode = models.CharField(max_length=50)
    view_count = models.CharField(max_length=50)
    image_url = models.URLField()
    url = models.URLField()
    publish_time = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    

class Manga(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    img = models.URLField()
    num = models.CharField(max_length=50)
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
