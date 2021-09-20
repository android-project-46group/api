import requests
from bs4 import BeautifulSoup


def scrapingDetailedInfo():

    ## アクセスするurl
    TOP_URL = 'https://www.nogizaka46.com/member'

    # BeautifulSoupオブジェクト生成
    headers = {'User-Agent': 'Mozilla/5.0'}

    # メインページの情報から、個人の情報がまとめられているところをとってくる
    soup = BeautifulSoup(
        requests.get(TOP_URL, headers=headers).content,'html.parser')
    details = soup.findAll('div', class_='unit')

    infos = {}
    JAPANESE_NAME_TAG = '名前'
    PERSONAL_INFO_TAG = ["生年月日", "血液型", '星座', '身長']
    for detail in details:
        person = {}

        href = detail.find("a").get("href")
        name_en = href[9:-4]

        print(f'scraping {name_en}...')

        # 詳細情報の含まれる URL を特定し情報をとってくる
        memberURL = href[1:]
        URL = TOP_URL + memberURL
        soup = BeautifulSoup(
            requests.get(URL, headers=headers).content, 'html.parser')

        profiles = soup.find('div', id='profile')
        name_ja = ' '.join(profiles.find('h2').text.split()[2:4])
        person[JAPANESE_NAME_TAG] = name_ja

        # personal info のなかの dd タグに、必要な情報が順番に含まれている
        profile = profiles.findAll('dd')
        for info_tag, data in zip(PERSONAL_INFO_TAG, profile):
            person[info_tag] = data.text

        infos[name_en] = person

    return infos


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
