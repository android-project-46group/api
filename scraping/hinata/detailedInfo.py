from pykakasi.legacy import kakasi
import requests
from bs4 import BeautifulSoup
import pykakasi


def scrapingDetailedInfo():

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

        profiles = soup.find('div', class_='p-member__info')
        person[JAPANESE_NAME_TAG] = name_ja

        # personal info のなかの td タグに、必要な情報が順番に含まれている
        # td タグは (key, value) * 五個あって、
        # ]「生年月日、星座、身長、出身地、血液型」の順
        data = profiles.findAll('td')
        num_data = len(data) // 2
        for i in range(num_data):
            tag_name = data[2*i].text.strip()
            info = data[2*i+1].text.strip()
            if tag_name != '出身地':
                person[tag_name] = info

        infos[name_en] = person

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


def main():
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


if __name__ == '__main__':
    main()
