import requests
from bs4 import BeautifulSoup
import pykakasi


def scrapingDetailedInfo():

    ## アクセスするurl
    BASE_URL = 'https://sakurazaka46.com'
    TOP_URL = 'https://sakurazaka46.com/s/s46/diary/blog/list?ima=1010'

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

        # shortUrl = './renka.iwamoto'
        shortUrl = unit.get("value")
        separatedName = unit.text.split('(')  # ['.', 'renka.iwamoto']
        if len(separatedName) == 0:
            continue
        name_ja = separatedName[0]
        print(name_ja, shortUrl)
        url = BASE_URL + shortUrl

        infos[name_ja] = url

    return infos


def NameLists():

    NamesUrl = 'https://sakurazaka46.com/s/s46/search/artist'

    # BeautifulSoupオブジェクト生成
    headers = {'User-Agent': 'Mozilla/5.0'}

    # メインページの情報から、個人の情報がまとめられているところをとってくる
    soup = BeautifulSoup(
        requests.get(NamesUrl, headers=headers).content,'html.parser')
    details = soup.findAll('li', class_='box')

    infos = {}

    BASE_URL = 'https://sakurazaka46.com'
    for detail in details:
        person = {}

        href = detail.find("a").get("href")

        # li の中には、name, kana の順番で格納されている
        p_tags = detail.findAll('p')
        name_ja = p_tags[0].text
        name_kana = p_tags[1].text

        name_en = kana2latin(name_kana)

        print(f'scraping {name_en}...')

        # 詳細情報の含まれる URL を特定し情報をとってくる
        URL = BASE_URL + href
        soup = BeautifulSoup(
            requests.get(URL, headers=headers).content, 'html.parser')


        infos[name_ja] = name_en
    return infos

def kana2latin(kana):
    kks = pykakasi.kakasi()
    result = kks.convert(kana)

    # [1] は半角スペースが入っている
    last = result[0]['hepburn']
    first = result[2]['hepburn']

    return last + first


if __name__ == '__main__':
    # スクレイピングを実行する
    detailed_infos = scrapingDetailedInfo()
    names = NameLists()

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
