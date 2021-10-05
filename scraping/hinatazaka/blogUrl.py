import requests
from bs4 import BeautifulSoup
import pykakasi



def scrapingDetailedInfo():

    ## アクセスするurl
    BASE_URL = 'https://hinatazaka46.com'
    TOP_URL = 'https://www.hinatazaka46.com/s/official/diary/member?ima=0000'

    # BeautifulSoupオブジェクト生成
    headers = {'User-Agent': 'Mozilla/5.0'}

    # メインページの情報から、個人の情報がまとめられているところをとってくる
    soup = BeautifulSoup(
        requests.get(TOP_URL, headers=headers).content,'html.parser')

    units = soup.findAll('option')

    print(len(units))
    infos = {}

    for unit in units:
        if unit.text == '- - -':
            continue
        if unit.text == '\n                          - - -\n                        ':
            continue

        # shortUrl = './renka.iwamoto'
        shortUrl = unit.get("value")
        if shortUrl == '/s/official/diary/member/list?ima=0000&ct=000':
            continue

        separatedName = unit.text.split('(')  # ['.', 'renka.iwamoto']
        if len(separatedName) == 0:
            continue
        name_ja = separatedName[0]
        print(name_ja, shortUrl)
        url = BASE_URL + shortUrl

        infos[name_ja] = url

    return infos


import pykakasi


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
    JAPANESE_NAME_TAG = '名前'
    PERSONAL_INFO_TAG = ["生年月日", "血液型", '星座', '身長']
    BASE_URL = 'https://www.hinatazaka46.com'
    for detail in details:
        person = {}

        href = detail.find("a").get("href")

        # li の中には、thumb(div>img), name, kana の順番で div が格納されている
        div_tags = detail.findAll('div')
        name_ja = div_tags[1].text.strip()
        name_kana = div_tags[2].text.strip()

        name_en = kana2latin(name_kana)

        print(f'scraping {name_en}...')

        # 詳細情報の含まれる URL を特定し情報をとってくる
        URL = BASE_URL + href
        soup = BeautifulSoup(
            requests.get(URL, headers=headers).content, 'html.parser')

        person[JAPANESE_NAME_TAG] = name_ja

        infos[name_ja] = name_en

        # 予想より多く detail が取れているみたいなので
        # 無理矢理最後のメンバーで終わらせる
        if name_ja == '山口 陽世':
            break

    return infos


# なぜか間にスペースが入る関係で、first を -1 からとってる
def kana2latin(kana):
    kks = pykakasi.kakasi()
    result = kks.convert(kana)

    # [1] は半角スペースが入っている
    last = result[0]['hepburn']
    first = result[-1]['hepburn']

    return last + first


if __name__ == '__main__':
    # スクレイピングを実行する
    detailed_infos = scrapingDetailedInfo()
    names = NameLists()
    print(detailed_infos)
    print(names)

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
            if cnt != MAX_COUNT:
                f.write(f'{TAB}"{names[name_ja]}": "{detailed_infos[name_ja]}",{NEW_LINE}')
            else:
                f.write(f'{TAB}"{names[name_ja]}": "{detailed_infos[name_ja]}"{NEW_LINE}')
        f.write(f'{DICT_END}{NEW_LINE}')
