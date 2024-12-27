import requests
import base64
import random
import time
from requests import Session
from bs4 import BeautifulSoup
from lxml import etree
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync


session = Session()

def get_user_agent():
     with open('user-agents.txt', 'r', encoding='utf8') as f:
        user_agent = random.choice(f.readlines())
        return user_agent.strip()

def get_photos_links():
    url = 'https://script.google.com/macros/s/AKfycbxmJcvTM3pk8cPyDREiLkI9ETNPWUAvGg2eKpyBbtXFZWlRp1iMwTFDa5N9rhdOJTPx1A/exec'
    response = requests.get(url)
    return response.json()['links']

def download_photo(link):
    img_data = requests.get(link).content
    img_name = link.split('/')[-1].split('.')[0]
    with open(f"photos/{img_name}.jpg", 'wb') as f:
        f.write(img_data)
    return f"photos/{img_name}.jpg"

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image

def search_image_on_alibaba(image_path):
    url = "https://open-s.alibaba.com/openservice/appImageSearchPicUrlUtilsService"
    base64_image = encode_image_to_base64(image_path)
    pic_url = f"data:image/jpeg;base64,{base64_image}"
    
    payload = {
        'picUrl': pic_url
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'Referrer': 'https://www.alibaba.com/',
    }

    response = session.post(url, data=payload, headers=headers)

    json_data=response.json()

    img=json_data['data']['imagePath']

    url=f"https://www.alibaba.com/picture/search.htm?imageType=oss&escapeQp=true&imageAddress={img}&sourceFrom=imageupload&uploadType=picDrag&SearchScene=home_new_user_first_screen@@FY23SearchBar&spm=a2700.product_home_newuser"
    
    with open('urls.txt', 'a') as f:
        f.write(url)

    response = session.get(url, headers=headers)
    
    if 'captcha' in response.text:
        print(12312)
        with sync_playwright() as p:
            browser = p.firefox.launch(headless = False)
            context = browser.new_context()
            page = context.new_page()
            stealth_sync(page)
            # page.add_init_script('Object.defineProperty(navigator,"webdriver",{get: () => undefined})')
            page.goto(url)
            # page.wait_for_selector("//span[contains(@id, 'nc_1_n1z')]", timeout=10000)
            # page.("//span[contains(@id, 'nc_1_n1z')]")
            # slider = page.locator("//span[contains(@id, 'nc_1__scale_text')]").bounding_box()
            handle = page.locator("//span[contains(@id, 'nc_1_n1z')]").bounding_box()
            start_x = handle['x'] + handle['width'] / 2
            start_y = handle['y'] + handle['height'] / 2
            end_x = start_x + 500

            time.sleep(5)

            page.mouse.move(start_x, start_y)
            page.mouse.down()

            # Переместите слайдер
            # page.mouse.move(end_x, start_y+50, steps=5)
            steps = 30

            # Вычислите смещение за каждый шаг
            step_x = (end_x - start_x) / steps
            step_y = 0  # Если движение строго по горизонтали

            for _ in range(steps):
                new_x = start_x + step_x
                new_y = start_y + step_y
                page.mouse.move(new_x, new_y)
                start_x, start_y = new_x, new_y
                time.sleep(random.uniform(0.01, 0.03))  # Добавьте небольшую задержку для плавности

            # Отпустите слайдер
            time.sleep(20)
    
    response = session.get(url, headers=headers)
    with open('resp.txt', 'w', encoding='utf8') as f:
        f.write(response.text)
    
    return response.text

def get_product_link(html):
    return html.split('<div class="card-info gallery-card-layout-info"><a href="')[1].split('" target="_blank"')[0]

def get_product_page(link):
    response = session.get('https:' + link)
    return response.text


        