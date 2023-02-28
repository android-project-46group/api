import requests
from bs4 import BeautifulSoup
import urllib.request
import json


SAVE_DIR_NAME = "face_img"

headers = {'User-Agent': 'Mozilla/5.0'}


def scrapingDetailedInfo():

    # アクセスするurl
    url = "https://www.nogizaka46.com/s/n46/api/list/member"

    # メインページの情報から、個人の情報がまとめられているところをとってくる
    soup = BeautifulSoup(
        requests.get(url, headers=headers).content, 'html.parser')
    str_soup = str(soup)
    json_soup = str_soup[4:-2]
    dict_soup = json.loads(json_soup)
    return dict_soup['data']


if __name__ == '__main__':
    # スクレイピングを実行する
    detailed_infos = scrapingDetailedInfo()
    with open("raw.json", mode="w") as f:
        json.dump(detailed_infos, f, indent=2)

    results = {}
    for detailed in detailed_infos:

        name_ja = detailed["name"]
        print(name_ja)
        if name_ja == "乃木坂46":
            continue

        result = {}
        result["name_ja"] = name_ja
        result["birthday"] = detailed["birthday"]
        result["blood_type"] = detailed["blood"]
        result["generation"] = detailed["cate"]
        result["graduation"] = detailed["graduation"]
        result["blog_url"] = ""
        name_en = detailed["english_name"]
        en = name_en.replace(" ", "")
        result["img_url"] = f"https://kokoichi0206.mydns.jp/imgs/nogi/{name_en}.jpeg"

        img_url = detailed["img"]
        urllib.request.urlretrieve(
            img_url, f'./{SAVE_DIR_NAME}/' + en + '.jpeg')

        if detailed["graduation"] == "NO":
            url = detailed["link"]
            soup = BeautifulSoup(
                requests.get(url, headers=headers).content, 'html.parser')
            dds = soup.findAll("dd")
            for dd in dds:
                txt = dd.text.strip()
                if txt[-2:] == "cm":
                    result["height"] = txt
        else:
            # 卒業生はリンクが存在せず、身長を取得できない
            result["height"] = "999cm"
        results[en] = result

    with open("detailed.json", mode="w") as f:
        json.dump(results, f, indent=2)


    # with open('names.txt', mode='w') as g:
    #     for name_en, detailed_info in detailed_infos.items():
    #         g.write(f'{name_en}{NEW_LINE}')
