import requests
import urllib.request
import os
from bs4 import BeautifulSoup
import json


# 一人用
def scraping_img_and_time_one(name, url):

    SAVE_DIR_NAME = 'imgs/hinata'

    # BeautifulSoupオブジェクト生成
    headers = {"User-Agent": "Mozilla/5.0"}

    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')

    # article より group で取っておくと、万が一最新の投稿に写真がなくても次以降を探しに行ける
    # top_sheet = soup.findAll('div', class_='p-blog-article')
    top_sheet = soup.findAll('div', class_='p-blog-group')

    latest_post_time = top_sheet[0].find(class_='c-blog-article__date').text.strip()
    latest_post_img_url = top_sheet[0].find('img').attrs['src']

    urllib.request.urlretrieve(
        latest_post_img_url, f'./{SAVE_DIR_NAME}/' + name + '.jpeg')


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
    with open(f"../{group_name}/blogUrls.txt", mode='rt', encoding='utf-8') as f:
        blog_url_infos = json.load(f)

    # print(scraping_img_and_time_one("kanemuramiku", "https://hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=12"))


    blog_infos = scraping_img_and_time_all(blog_url_infos)

    TAB         = '\t'
    NEW_LINE    = '\n'
    DICT_START  = '{'
    DICT_END    = '}'
    with open('blog_infos_hinatazaka.txt', mode='w') as f:
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
