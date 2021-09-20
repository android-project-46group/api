import requests
import urllib.request
import os
from bs4 import BeautifulSoup
import pykakasi


# 全メンバーの顔写真を取得
def scraping_allpic():

    ## artist なの、乃木坂と違いあって面白い
    TOP_URL = 'https://sakurazaka46.com/s/s46/search/artist'

    # BeautifulSoupオブジェクト生成
    headers = {'User-Agent': 'Mozilla/5.0'}

    # メインページの情報から、個人の情報がまとめられているところをとってくる
    soup = BeautifulSoup(
        requests.get(TOP_URL, headers=headers).content,'html.parser')
    details = soup.findAll('li', class_='box')

    SAVE_DIR_NAME = 'Pictures'
    # 写真保存用のフォルダが存在しない場合、フォルダを作成
    if not os.path.isdir(SAVE_DIR_NAME):
        print("created folder")
        os.mkdir(SAVE_DIR_NAME)

    BASE_URL = 'https://sakurazaka46.com'

    for detail in details:
        href = detail.find("a").get("href")

        # li の中には、name, kana の順番で格納されている
        p_tags = detail.findAll('p')
        name_ja = p_tags[0].text
        name_kana = p_tags[1].text

        name_en = kana2latin(name_kana)

        img = detail.find('img')

        img_url = BASE_URL + img.attrs['src']
        urllib.request.urlretrieve(
            img_url, f'./{SAVE_DIR_NAME}/' + name_en + '.jpeg')

# うえむら りな -> uemurarina
def kana2latin(kana):
    kks = pykakasi.kakasi()
    result = kks.convert(kana)

    # [1] は半角スペースが入っている
    last = result[0]['hepburn']
    first = result[2]['hepburn']

    return last + first


if __name__ == '__main__':
    scraping_allpic()
