import requests
from bs4 import BeautifulSoup
from .models import Manga

def update_manga_data():
    url = "https://www.manhuagui.com/update/"
    try:
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, "lxml")
        main = soup.find("div", class_="latest-cont")
        items = main.find("div", class_="latest-list").find_all("li")

        # 清空舊資料
        Manga.objects.all().delete()

        for m in items:
            title = m.find("a").get("title")
            link = "https://www.manhuagui.com/" + m.find("a").get("href")
            img = m.find("img").get("src")
            num = m.find("span", class_="tt").text
            Manga.objects.create(title=title, url=link, img=img, num=num)
        print("✅ 漫畫資料已更新")
    except Exception as e:
        print("❌ 漫畫資料更新失敗", e)
