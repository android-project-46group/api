import requests
import urllib.request
import os
from bs4 import BeautifulSoup


# 全メンバーの顔写真を取得
def scraping_allpic():

    ## アクセスするurl
    TOP_URL = "https://www.nogizaka46.com/member"

    SAVE_DIR_NAME = 'Pictures'
    # 写真保存用のフォルダが存在しない場合、フォルダを作成
    if not os.path.isdir(SAVE_DIR_NAME):
        print("created folder")
        os.mkdir(SAVE_DIR_NAME)


    # BeautifulSoupオブジェクト生成
    headers = {"User-Agent": "Mozilla/5.0"}

    soup = BeautifulSoup(requests.get(TOP_URL, headers=headers).content, 'html.parser')
    details = soup.findAll("div", class_="unit")

    for detail in details:
        href = detail.find("a").get("href")
        memberURL = href[1:]
        name = href[9:-4]

        accessURL = TOP_URL + memberURL

        soup = BeautifulSoup(requests.get(accessURL, headers=headers).content, 'html.parser')
        content = soup.find(id='profile')
        img = content.find('img')
        print(content)

        urllib.request.urlretrieve(
            img.attrs['src'], f'./{SAVE_DIR_NAME}/' + name + '.jpeg')


if __name__ == '__main__':
    scraping_allpic()
