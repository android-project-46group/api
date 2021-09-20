from pykakasi.legacy import kakasi
import requests
from bs4 import BeautifulSoup
import pykakasi


def scrapingDetailedInfo():

    ## artist なの、乃木坂と違いあって面白い
    TOP_URL = 'https://sakurazaka46.com/s/s46/search/artist'

    # BeautifulSoupオブジェクト生成
    headers = {'User-Agent': 'Mozilla/5.0'}

    # メインページの情報から、個人の情報がまとめられているところをとってくる
    soup = BeautifulSoup(
        requests.get(TOP_URL, headers=headers).content,'html.parser')
    details = soup.findAll('li', class_='box')

    infos = {}
    JAPANESE_NAME_TAG = '名前'
    PERSONAL_INFO_TAG = ["生年月日", "血液型", '星座', '身長']
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

        profiles = soup.find('div', class_='prof-elem')
        person[JAPANESE_NAME_TAG] = name_ja

        # personal info のなかの dd タグに、必要な情報が順番に含まれている
        # dd タグは五個あって、「生年月日、星座、身長、出身地、血液型」の順
        profile_tags = profiles.findAll('dt')
        profiles = profiles.findAll('dd')
        for tag, data in zip(profile_tags, profiles):
            tag_name = tag.text
            if tag_name != '出身地':
                person[tag_name] = data.text

        infos[name_en] = person

    return infos


# うえむら りな -> uemurarina
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
    print(detailed_infos)

    # detailed_info には、次のような情報が入っている
    ## key = 'akimotomanatsu'
    ## value = {'生年月日': '1993年8月20日', '血液型': 'B型', '星座': 'しし座', '身長': '154cm'}

    TAB         = '\t'
    NEW_LINE    = '\n'
    DICT_START  = '{'
    DICT_END    = '}'
    with open('detailed_infos.txt', mode='w') as f:
        f.write(f'{DICT_START}{NEW_LINE}')
        for name_en, detailed_info in detailed_infos.items():
            f.write(f'{TAB}"{name_en}": {DICT_START}{NEW_LINE}')
            for info_tag, data in detailed_info.items():
                f.write(f'{TAB}{TAB}"{info_tag}": "{data}",{NEW_LINE}')
            f.write(f'{TAB}{DICT_END},{NEW_LINE}')
        f.write(f'{DICT_END}{NEW_LINE}')


    with open('names.txt', mode='w') as g:
        for name_en, detailed_info in detailed_infos.items():
            g.write(f'{name_en}{NEW_LINE}')
