from django.core.management.base import BaseCommand
from mainapp.models import AnimeCard  # 請確認你已建立 AnimeCard model
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Command(BaseCommand):
    help = "使用 Selenium 爬取動畫資料，寫入 AnimeCard 資料表"

    def handle(self, *args, **kwargs):
        url = "https://ani.gamer.com.tw/"
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        service = Service(executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        time.sleep(2)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "anime-content-block"))
            )
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, "lxml")
            main = soup.find_all("div", class_="anime-content-block")[:20]

            AnimeCard.objects.all().delete()  # 先清除舊資料

            for m in main:
                try:
                    name = m.find("p", class_="anime-name").text.strip()
                    num = m.find("div", class_="anime-episode").find("p").text.strip()
                    view = m.find("div", class_="anime-watch-number").find("p").text.strip()
                    link = "https://ani.gamer.com.tw/" + m.find("div", class_="anime-block").find("a").get("href")
                    img_tag = m.find("div", class_="anime-blocker").find("img")
                    img = img_tag.get("data-src") or img_tag.get("src")
                    times = m.find("div", class_="anime-hours-block").find("span").text.strip()

                    AnimeCard.objects.create(
                        title=name,
                        episode=num,
                        view_count=view,
                        image_url=img,
                        url=link,
                        publish_time=times
                    )
                except Exception as e:
                    print(f"❌ 錯誤跳過一筆: {e}")
        except Exception as e:
            print(f"❌ 爬蟲整體失敗: {e}")
        finally:
            driver.quit()

        self.stdout.write(self.style.SUCCESS("✅ 動畫資料寫入 AnimeCard 完成"))
