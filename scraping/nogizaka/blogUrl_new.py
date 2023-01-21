import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import json


BASE_URL = 'https://nogizaka46.com'

def scrapingDetailedInfo():

    ## アクセスするurl
    TOP_URL = 'https://www.nogizaka46.com/s/n46/diary/MEMBER'

    # BeautifulSoupオブジェクト生成
    headers = {'User-Agent': 'Mozilla/5.0'}

    # メインページの情報から、個人の情報がまとめられているところをとってくる
    soup = BeautifulSoup(
        requests.get(TOP_URL, headers=headers).content,'html.parser')

    atags = soup.findAll('a', class_='ba--ml__one__a')

    print(len(atags))
    infos = {}

    excluded = [
        "新4期生",
        "４期生",
        "３期生",
        "研究生",
        "運営スタッフ",
    ]
    for atag in atags:

        name = atag.text.strip()

        if name in excluded:
            continue

        url = atag.get("href")

        member_blog_url = urllib.parse.urljoin(BASE_URL, url)
        getLatestBlog(member_blog_url, name)

        infos[name] = member_blog_url

    return infos


def getLatestBlog(url, name):

    print("getLatestBlog called")
    print(f"url: {url}, name: {name}")
    # BeautifulSoupオブジェクト生成
    headers = {'User-Agent': 'Mozilla/5.0'}

    # メインページの情報から、個人の情報がまとめられているところをとってくる
    sp = BeautifulSoup(
        requests.get(url, headers=headers).content,'html.parser')
    latest = sp.find('a', class_='bl--card')
    print(latest)

    SAVE_IMG_DIR = "img"

    infos = {}


    div_img = latest.find("div", class_="m--bg")
    print(div_img)
    img_url = div_img.get("data-src")
    print(img_url)

    div_title = latest.find("p", class_="bl--card__ttl")
    print(div_title)
    title = div_title.text.strip()
    print(f"title: {title}")

    # 写真を保存する
    if img_url[0:4] != "http":
        img_url = urllib.parse.urljoin(BASE_URL, img_url)

    try:
        urllib.request.urlretrieve(
            img_url, f'{SAVE_IMG_DIR}/{name}.jpeg')
    except:
        print(f"failed to download img url: {img_url}")

    return infos


if __name__ == '__main__':

    with open('./detailed_infos.txt') as f:
        md = json.load(f)
    print(md)

    # スクレイピングを実行する
    detailed_infos = scrapingDetailedInfo()
    print(detailed_infos)

    TAB         = '\t'
    NEW_LINE    = '\n'
    DICT_START  = '{'
    DICT_END    = '}'
    with open('blogUrls.txt', mode='w') as f:
        MAX_COUNT = len(detailed_infos)
        cnt = 0
        f.write(f'{DICT_START}{NEW_LINE}')
        for name_ja, blogUrl in detailed_infos.items():
            cnt += 1

            name_en = ""
            for k, v in md.items():
                if v['名前'] == name_ja:
                    name_en = k
            if name_en == "":
                name_en = name_ja

            if cnt != MAX_COUNT:
                f.write(f'{TAB}"{name_en}": "{detailed_infos[name_ja]}",{NEW_LINE}')
                # f.write(f'{TAB}"{names[name_ja]}": "{detailed_infos[name_ja]}",{NEW_LINE}')
            else:
                f.write(f'{TAB}"{name_en}": "{detailed_infos[name_ja]}"{NEW_LINE}')
        f.write(f'{DICT_END}{NEW_LINE}')
