import requests
from bs4 import BeautifulSoup
import json


def scrapingColorsSource1():

    ## アクセスするurl
    TOP_URL = "https://senublog.com/nogizaka46-live-psylliumcolor-call/"

    # BeautifulSoupオブジェクト生成
    headers = {'User-Agent': 'Mozilla/5.0'}

    soup = BeautifulSoup(
        requests.get(TOP_URL, headers=headers).content,'html.parser')
    units = soup.findAll('div', class_='st-mybox-class')

    infos = {}

    print(units)

    for unit in units:
        name = unit.find("p", class_="st-mybox-title").text
        print(name)
        divs = unit.find("div", class_="st-in-mybox")
        for div in divs:
            t = div.text
            if "カラー：" in t:
                infos[name] = t.strip("カラー：").split("×")

    return infos

def scrapingColorsSource1():

    ## アクセスするurl
    TOP_URL = "https://senublog.com/nogizaka46-live-psylliumcolor-call/"

    # BeautifulSoupオブジェクト生成
    headers = {'User-Agent': 'Mozilla/5.0'}

    soup = BeautifulSoup(
        requests.get(TOP_URL, headers=headers).content,'html.parser')
    units = soup.findAll('div', class_='st-mybox-class')

    infos = {}

    print(units)

    for unit in units:
        name = unit.find("p", class_="st-mybox-title").text
        print(name)
        divs = unit.find("div", class_="st-in-mybox")
        for div in divs:
            t = div.text
            if "カラー：" in t:
                infos[name] = t.strip("カラー：").split("×")

    return infos


if __name__ == '__main__':
    infos = scrapingColorsSource1()

    with open(f'./nogi.json', 'w') as f:
        json.dump(infos, f, indent=2, ensure_ascii=False)
