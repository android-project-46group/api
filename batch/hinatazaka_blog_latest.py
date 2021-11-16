import requests
import urllib.request
import os
from bs4 import BeautifulSoup
import json
import time


# 一人用
def scraping_img_and_time_one(name, url):
    time.sleep(1)

    SAVE_DIR_NAME = 'imgs/hinata'

    # BeautifulSoupオブジェクト生成
    headers = {"User-Agent": "Mozilla/5.0"}


   # =============== 更新日時を取ってくるパート ===================
    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
    # article より group で取っておくと、万が一最新の投稿に写真がなくても次以降を探しに行ける
    # top_sheet = soup.findAll('div', class_='p-blog-article')
    top_sheet = soup.findAll('div', class_='p-blog-group')

    # =============== 写真を取ってくるパート ===================
    OFFICIAL_ICON_URL = "https://img.nogizaka46.com/blog/pic/n46_list.jpg"

    latest_post_time = top_sheet[0].find(class_='c-blog-article__date').text.strip()
    latest_post_img_url = top_sheet[0].find('img').attrs['src']

    # TODO: heic 形式も保存できるようにする
    if latest_post_img_url[-4:] == "heic":
        latest_post_img_url = "https://sakurazaka46.com/files/14/s46/img/com-logo_pc.svg"

    print(latest_post_img_url)
    urllib.request.urlretrieve(
        latest_post_img_url, f'/home/ubuntu/work/python/api/batch/{SAVE_DIR_NAME}/' + name + '.jpeg')

    return latest_post_time


def scraping_img_and_time_all(blog_url_infos):
    PIC_BASE_URL = 'https://kokoichi0206.mydns.jp/imgs/blog/hinata/'
    blog_infos = {}
    for name, url in blog_url_infos.items():
        latest_time = scraping_img_and_time_one(name, url)
        blog_info = {}
        blog_info['last_updated_at'] = latest_time
        blog_info['pic_url'] = PIC_BASE_URL + name + '.jpeg'

        blog_infos[name] = blog_info

    return blog_infos


if __name__ == '__main__':
    group_name = 'hinatazaka'
    with open(f"/home/ubuntu/work/python/api/scraping/{group_name}/blogUrls.txt", mode='rt', encoding='utf-8') as f:
        blog_url_infos = json.load(f)

    blog_infos = scraping_img_and_time_all(blog_url_infos)

    with open(f'/home/ubuntu/work/python/api/batch/blog_infos/hinatazaka.txt', 'w') as f:
        json.dump(blog_infos, f, indent=2)
