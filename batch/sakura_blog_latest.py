import requests
import urllib.request
import os
from bs4 import BeautifulSoup
import json
import time


# 一人用
def scraping_img_and_time_one(name, url):
    time.sleep(1)

    SAVE_DIR_NAME = 'imgs/sakura'

    SAKURA_BASE_URL = 'https://sakurazaka46.com'

    # BeautifulSoupオブジェクト生成
    headers = {"User-Agent": "Mozilla/5.0"}

    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')

    top_sheet = soup.findAll('ul', class_='com-blog-part')

    detailed_url = top_sheet[0].find('a').attrs['href']

    url = SAKURA_BASE_URL + detailed_url
    detailed = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')

    # =============== 更新日時を取ってくるパート ===================
    time_sheet = detailed.findAll('div', class_='blog-foot')[0]
    latest_post_time = time_sheet.find(class_='date').text

    # =============== 写真を取ってくるパート ===================
    # 写真が見つからないメンバーは公式写真を入れておく！
    OFFICIAL_ICON_URL = 'https://sakurazaka46.com/files/14/s46/img/blog-thumb-empty.png'
    url = OFFICIAL_ICON_URL

    img_sheet = detailed.findAll('div', class_='box-article')[0]
    latest_post_img_url_elm = img_sheet.find('img')

    if latest_post_img_url_elm:
        latest_post_img_url = latest_post_img_url_elm.attrs['src']
        url = SAKURA_BASE_URL + latest_post_img_url

    # TODO: heic 形式も保存できるようにする
    if url[-4:] == "heic":
        url = OFFICIAL_ICON_URL

    print(url)
    urllib.request.urlretrieve(
        url, f'/home/ubuntu/work/python/api/batch/{SAVE_DIR_NAME}/' + name + '.jpeg')

    return latest_post_time


def scraping_img_and_time_all(blog_url_infos):
    PIC_BASE_URL = 'https://kokoichi0206.mydns.jp/imgs/blog/sakura/'
    blog_infos = {}
    for name, url in blog_url_infos.items():
        latest_time = scraping_img_and_time_one(name, url)
        blog_info = {}
        blog_info['last_updated_at'] = latest_time
        blog_info['pic_url'] = PIC_BASE_URL + name + '.jpeg'

        blog_infos[name] = blog_info

    return blog_infos


if __name__ == '__main__':
    group_name = 'sakurazaka'
    with open(f"/home/ubuntu/work/python/api/scraping/{group_name}/blogUrls.txt", mode='rt', encoding='utf-8') as f:
        blog_url_infos = json.load(f)

    print(blog_url_infos)
    blog_infos = scraping_img_and_time_all(blog_url_infos)

    with open(f'/home/ubuntu/work/python/api/batch/blog_infos/sakurazaka.txt', 'w') as f:
        json.dump(blog_infos, f, indent=2)
