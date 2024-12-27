import os
import random
from utils import *
import json

if __name__ == '__main__':
    count=0
    for link in get_photos_links():
        photo_path = download_photo(link)
        html = search_image_on_alibaba(photo_path)

        os.remove(photo_path)

        product_link = get_product_link(html)

        with open('page.txt', 'w',encoding='utf8') as f:
            f.write(get_product_page(product_link))
        print(count)
        if count >50:
            break
        count+=1
    