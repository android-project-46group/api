from os import name
from pykakasi.legacy import kakasi
import requests
from bs4 import BeautifulSoup
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials

# JSONのパス (XXXXX, YYYYY は任意の文字列)
JSON_PATH = 'serviceAccountKey.json'

# 初期化
cred = credentials.Certificate(JSON_PATH)
firebase_admin.initialize_app(cred)

db = firestore.client()


def scrapingFormation(name_lists, single):

    # URL 構成の感じ、めっちゃ桜坂と似てる！！
    TOP_URL = 'https://www.hinatazaka46.com/s/official/diary/formation/list?ima=0000'

    # BeautifulSoupオブジェクト生成
    headers = {'User-Agent': 'Mozilla/5.0'}

    # メインページの情報から、個人の情報がまとめられているところをとってくる
    soup = BeautifulSoup(
        requests.get(TOP_URL, headers=headers).content,'html.parser')
    songs = soup.findAll('div', class_=f'{single}_single')

    formations = []
    JAPANESE_NAME_TAG = '名前'
    BASE_URL = 'https://www.hinatazaka46.com'


    for song in songs:
        title_str = song.find("h4").text
        titles = getTitles(title_str)
        for title in titles:
            formation = {}
            formation['single'] = single
            formation['title'] = title

            # li の中には、thumb(div>img), name, kana の順番で div が格納されている
            rows = song.findAll('ul')
            # formation['rows'] = []
            # XYZ: Z が１列目, Y が２列目, X が３列目
            tmp = []
            for row in rows:

                row_name = row.get("class")[0]

                digit = 1
                if row_name == 'second':
                    digit = 10 ** 1
                elif row_name == 'third':
                    digit = 10 ** 2


                cnt = 1
                lis = row.findAll('li')
                for li in lis:
                    position = str(cnt * digit).zfill(3)
                    t = {
                        "position": position,
                        "name_ja": li.text,
                        "name_en": name_lists[li.text]
                    }
                    tmp.append(t)

                    cnt += 1

            formation['positions'] = tmp

            formations.append(formation)

    return formations


import pykakasi


# {"上村ひなの": "kamimurahinano", ...}
def NameLists():

    # URL 構成の感じ、めっちゃ桜坂と似てる！！
    TOP_URL = 'https://www.hinatazaka46.com/s/official/search/artist'

    # BeautifulSoupオブジェクト生成
    headers = {'User-Agent': 'Mozilla/5.0'}

    # メインページの情報から、個人の情報がまとめられているところをとってくる
    soup = BeautifulSoup(
        requests.get(TOP_URL, headers=headers).content,'html.parser')
    details = soup.findAll('li', class_='p-member__item')

    infos = {}

    BASE_URL = 'https://www.hinatazaka46.com'
    for detail in details:

        href = detail.find("a").get("href")

        # li の中には、thumb(div>img), name, kana の順番で div が格納されている
        div_tags = detail.findAll('div')
        name_ja = div_tags[1].text.strip()
        name_kana = div_tags[2].text.strip()

        name_en = kana2latin(name_kana)

        if name_en[0] == '1':
            continue
        elif name_en[0] == '2':
            continue
        print(f'scraping {name_en}...')

        # 詳細情報の含まれる URL を特定し情報をとってくる
        URL = BASE_URL + href
        soup = BeautifulSoup(
            requests.get(URL, headers=headers).content, 'html.parser')

        name_ja = ''.join(name_ja.split(' '))

        infos[name_ja] = name_en


        # 予想より多く detail が取れているみたいなので
        # 無理矢理最後のメンバーで終わらせる
        if name_ja == '山口 陽世':
            break

    # 脱退メンバーを、手動で入れてあげる
    infos['井口眞緒'] = 'iguchimao'
    infos['柿崎芽実'] = 'kakizakimemi'
    return infos


# なぜか間にスペースが入る関係で、first を -1 からとってる
def kana2latin(kana):
    kks = pykakasi.kakasi()
    result = kks.convert(kana)

    # [1] は半角スペースが入っている
    last = result[0]['hepburn']
    first = result[-1]['hepburn']

    return last + first


# 「ってか」「思いがけないダブルレインボー」「アディショナルタイム」
#  → ['ってか', '思いがけないダブルレインボー', 'アディショナルタイム']
def getTitles(titles):
    a = titles.split('」「')
    ans = []
    for b in a:
        tmp = b
        if b[0] == '「':
            tmp = tmp[1:]
        if b[-1] == '」':
            tmp = tmp[:-1]
        ans.append(tmp)
    return ans


def main():
    # 日 → 英の変換をするための準備
    name_lists = NameLists()

    formation_infos = []
    # singles = ['1st', '2nd', '3rd', '4th', '5th', '6th']
    # singles = ['4th', '5th', '6th']   # 1st-3rd は井口がいるから省いた（写真とかない）
    singles = ['1st', '2nd', '3rd']
    for single in singles:
        # スクレイピングを実行する
        tmp = scrapingFormation(name_lists=name_lists, single=single)
        formation_infos += tmp

    print(formation_infos)

    for formation_info in formation_infos:
        title = formation_info['title']
        for position in formation_info['positions']:
            pos = position['position']
            doc_ref = db.collection('formations_hinata').document(f'{title}{pos}')
            doc_ref.set({
                u'single': formation_info['single'],
                u'title': formation_info['title'],
                u'position': position['position'],
                u'name_en': position['name_en'],
                u'name_ja': position['name_ja'],
            })

    # TAB         = '\t'
    # NEW_LINE    = '\n'
    # DICT_START  = '{'
    # DICT_END    = '}'
    # with open('formation_infos.txt', mode='w') as f:
    #     f.write(f'{DICT_START}{NEW_LINE}')
    #     for formation in formation_infos:
    #         f.write(f'{formation_infos}')


if __name__ == '__main__':
    res = main()
    print(res)
