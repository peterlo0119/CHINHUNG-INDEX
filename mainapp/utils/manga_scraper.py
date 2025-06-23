from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, os, django
from mainapp.models import Manga

# 初始化 Django 環境（只有在你單獨執行 .py 檔時才需要）
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ytstreamsite.settings")
django.setup()

def update_manga_data():
    print("🔄 update_manga_data() 開始更新漫畫資料...")

    url = "https://www.manhuagui.com/update/"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ Windows（本機）使用
    service = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")
    # ✅ 如果是 Render 要改為 /usr/bin/chromedriver
    # service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    # 懶加載觸發
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    main = soup.find("div", class_="latest-cont")
    items = main.find("div", class_="latest-list").find_all("li")

    Manga.objects.all().delete()  # 清空原資料

    for m in reversed(items):
        try:
            title = m.find("a").get("title")
            url = "https://www.manhuagui.com" + m.find("a").get("href")

            img_tag = m.find("img")
            img = ""
            if img_tag:
                img = img_tag.get("src") or img_tag.get("data-src") or ""
                if img.startswith("//"):
                    img = "https:" + img
                elif img.startswith("/"):
                    img = "https://www.manhuagui.com" + img

            num_tag = m.find("span", class_="tt")
            num = num_tag.text.strip() if num_tag else ""

            Manga.objects.create(title=title, url=url, img=img, num=num)
        except Exception as e:
            print(f"⚠️ 單筆錯誤略過：{e}")

    print("✅ Manga 資料更新完成")
