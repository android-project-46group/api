import requests
import urllib.request
import os
from bs4 import BeautifulSoup
import json


# 一人用
def scraping_img_and_time_one(name, url):

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

    print(url)
    urllib.request.urlretrieve(
        url, f'./{SAVE_DIR_NAME}/' + name + '.jpeg')

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
    with open(f"../{group_name}/blogUrls.txt", mode='rt', encoding='utf-8') as f:
        blog_url_infos = json.load(f)

    # print(scraping_img_and_time_one("watanaberika", "https://sakurazaka46.com/s/s46/diary/blog/list?ima=3344&ct=20"))

    blog_infos = scraping_img_and_time_all(blog_url_infos)

    TAB         = '\t'
    NEW_LINE    = '\n'
    DICT_START  = '{'
    DICT_END    = '}'
    with open('blog_infos_sakurazaka.txt', mode='w') as f:
        MAX_COUNT = len(blog_infos)
        cnt = 0
        f.write(f'{DICT_START}{NEW_LINE}')
        for name_en, blog_infos in blog_infos.items():
            cnt += 1
            f.write(f'{TAB}"{name_en}": {DICT_START}{NEW_LINE}')
            f.write(f'{TAB}{TAB}"last_updated_at": "{blog_infos["last_updated_at"]}",{NEW_LINE}')
            f.write(f'{TAB}{TAB}"pic_url": "{blog_infos["pic_url"]}"{NEW_LINE}')

            if cnt != MAX_COUNT:
                f.write(f'{TAB}{DICT_END},{NEW_LINE}')
            else:
                # 最後だけ、Json のルールに則って"," をつけない
                f.write(f'{TAB}{DICT_END}{NEW_LINE}')
        f.write(f'{DICT_END}{NEW_LINE}')
