import requests
import urllib.request
import os
from bs4 import BeautifulSoup
import pykakasi


# 全メンバーの顔写真を取得
def scraping_allpic():

    # URL 構成の感じ、めっちゃ桜坂と似てる！！
    TOP_URL = 'https://www.hinatazaka46.com/s/official/search/artist'

    # BeautifulSoupオブジェクト生成
    headers = {'User-Agent': 'Mozilla/5.0'}

    # メインページの情報から、個人の情報がまとめられているところをとってくる
    soup = BeautifulSoup(
        requests.get(TOP_URL, headers=headers).content,'html.parser')
    details = soup.findAll('li', class_='p-member__item')

    SAVE_DIR_NAME = 'Pictures'
    # 写真保存用のフォルダが存在しない場合、フォルダを作成
    if not os.path.isdir(SAVE_DIR_NAME):
        print("created folder")
        os.mkdir(SAVE_DIR_NAME)

    for detail in details:

        # li の中には、thumb(div>img), name, kana の順番で div が格納されている
        div_tags = detail.findAll('div')
        name_ja = div_tags[1].text.strip()
        name_kana = div_tags[2].text.strip()

        name_en = kana2latin(name_kana)

        img = detail.find('img')

        img_url = img.attrs['src']
        urllib.request.urlretrieve(
            img_url, f'./{SAVE_DIR_NAME}/' + name_en + '.jpeg')

        # 予想より多く detail が取れているみたいなので
        # 無理矢理最後のメンバーで終わらせる
        if name_ja == '渡辺 莉奈':
            break

def kana2latin(kana):
    kks = pykakasi.kakasi()
    result = kks.convert(kana)

    # [1] は半角スペースが入っている
    last = result[0]['hepburn']
    first = result[-1]['hepburn']

    return last + first


if __name__ == '__main__':
    scraping_allpic()
