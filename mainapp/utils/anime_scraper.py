from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time, os, django
from selenium.webdriver.chrome.options import Options
from mainapp.models import AnimeCard

# 初始化 Django 環境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ytstreamsite.settings")
django.setup()

def update_anime_data():
    print("🔄 update_anime_data() 開始更新動畫卡片...")

    url = "https://ani.gamer.com.tw/"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    #service = Service("/usr/bin/chromedriver")  # Render 用
    service = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")  # 本機用（Windows）

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, "lxml")
        blocks = soup.find_all("div", class_="anime-content-block")[:18]

        AnimeCard.objects.all().delete()

        for m in reversed(blocks):
            try:
                name = m.find("p", class_="anime-name").text.strip()
                num = m.find("div", class_="anime-episode").find("p").text.strip()
                view = m.find("div", class_="anime-watch-number").find("p").text.strip()
                url = "https://ani.gamer.com.tw/" + m.find("div", class_="anime-block").find("a").get("href")
                img = m.find("div", class_="anime-blocker").find("img").get("src")
                times = m.find("div", class_="anime-hours-block").find("span").text.strip()

                AnimeCard.objects.create(
                    title=name,
                    episode=num,
                    view_count=view,
                    image_url=img,
                    url=url,
                    publish_time=times
                )
            except Exception as e:
                print(f"⚠️ 單筆處理錯誤：{e}")

        print("✅ AnimeCard 已成功更新")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

    finally:
        driver.quit()
