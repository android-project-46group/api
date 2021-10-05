import requests
from bs4 import BeautifulSoup


def scrapingDetailedInfo():

    ## アクセスするurl
    TOP_URL = 'https://blog.nogizaka46.com/'

    # BeautifulSoupオブジェクト生成
    headers = {'User-Agent': 'Mozilla/5.0'}

    # メインページの情報から、個人の情報がまとめられているところをとってくる
    soup = BeautifulSoup(
        requests.get(TOP_URL, headers=headers).content,'html.parser')
    # sidemember = soup.find('div', id='sidemember')
    units = soup.findAll('div', class_='unit')

    print(len(units))
    infos = {}

    for unit in units:

        # shortUrl = './renka.iwamoto'
        shortUrl = unit.find("a").get("href")
        memberRelated = shortUrl.split('/')[1]  # ['.', 'renka.iwamoto']
        tmp = memberRelated.split('.')   # ['renka', 'iwamoto']

        memberUrl = TOP_URL + memberRelated
        name_en = tmp[1] + tmp[0]

        infos[name_en] = memberUrl

    return infos


if __name__ == '__main__':
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
        for name_en, blogUrl in detailed_infos.items():
            cnt += 1
            if cnt != MAX_COUNT:
                f.write(f'{TAB}"{name_en}": "{blogUrl}",{NEW_LINE}')
            else:
                f.write(f'{TAB}"{name_en}": "{blogUrl}"{NEW_LINE}')
        f.write(f'{DICT_END}{NEW_LINE}')
