import requests
import base64
import os
import pandas as pd
from bs4 import BeautifulSoup
from requests import Session

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image

def search_image_on_alibaba(image_path):
    # URL для отправки запроса (предположительно, URL может быть другим)
    url = "https://open-s.alibaba.com/openservice/appImageSearchPicUrlUtilsService"
    
    # Кодирование изображения в base64
    base64_image = encode_image_to_base64(image_path)
    
    # Формирование строки для picUrl
    pic_url = f"data:image/jpeg;base64,{base64_image}"
    
    # Полезная нагрузка
    payload = {
        'picUrl': pic_url
    }
    
    session = Session()

    # Отправка запроса POST
    response = session.post(url, data=payload)
    with open('log.txt', 'w') as f:
        f.write(response.text)

    json_data=response.json()
    img=json_data['data']['imagePath']
    print(img)

    url=f"https://www.alibaba.com/picture/search.htm?imageType=oss&escapeQp=true&imageAddress={img}&sourceFrom=imageupload&uploadType=picDrag&SearchScene=home_new_user_first_screen@@FY23SearchBar&spm=a2700.product_home_newuser"
    print(url)
    response=session.get(url)
    with open('resp.txt', 'w') as f:
        f.write(response.text)

    if response.status_code == 200:
        # Парсинг ответа для извлечения данных
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Поиск первого товара
        first_item = soup.find('div', class_='item-main')
        
        if first_item:
            item_name = first_item.find('h2').get_text()
            item_link = first_item.find('a')['href']
            supplier_info = first_item.find('div', class_='supplier-info').get_text()
            
            return {
                "name": item_name,
                "link": item_link,
                "supplier": supplier_info
            }
    
    return None

if __name__ == '__main__':
    search_image_on_alibaba('1.webp')