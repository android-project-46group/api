import requests
from bs4 import BeautifulSoup
import json


def scrapingColorsFrom2021_SAKURA(url):
    soup = getSoupObject(url)

    divs = soup.findAll('div', class_='sakura')[0]

    return findInfos(divs)

def scrapingColorsFrom2021_HINATA(url):
    soup = getSoupObject(url)

    divs = soup.findAll('div', class_='hinata')[0]

    return findInfos(divs)


def scrapingColorsFromKeyakiFes(url):
    soup = getSoupObject(url)
    return findInfos(soup)

def getSoupObject(url):
    # BeautifulSoupオブジェクト生成
    headers = {'User-Agent': 'Mozilla/5.0'}
    soup = BeautifulSoup(
        requests.get(url, headers=headers).content,'html.parser')

    return soup


def findInfos(elm):
    units = elm.findAll('div', class_='psyllium_text')
    infos = {}

    for unit in units:
        name = unit.find("h4").text
        colors = [c[1:] for c in unit.find("p").text.split("×")]
        infos[name] = colors

    return infos


if __name__ == '__main__':
    all_sakura = scrapingColorsFrom2021_SAKURA("https://www.hinatazaka46.com/s/official/diary/detail/39908")
    all_hinata = scrapingColorsFrom2021_HINATA("https://www.hinatazaka46.com/s/official/diary/detail/39908")

    sakura_2022 = scrapingColorsFromKeyakiFes("https://sakurazaka46.com/s/s46/diary/detail/44749?ima=0000&link=ROBO004&cd=wkf2022_cont")
    hinata_2022 = scrapingColorsFromKeyakiFes("https://www.hinatazaka46.com/s/official/diary/detail/44750?ima=0000&link=ROBO004&cd=wkf2022_cont")

    for name, colors in sakura_2022.items():
        all_sakura[name] = colors
    for name, colors in hinata_2022.items():
        all_hinata[name] = colors

    with open(f'./hinata.json', 'w') as f:
        json.dump(all_hinata, f, indent=2, ensure_ascii=False)
    with open(f'./sakura.json', 'w') as f:
        json.dump(all_sakura, f, indent=2, ensure_ascii=False)

    # all_2021 = scrapingColorsFromKeyakiFes("https://www.hinatazaka46.com/s/official/diary/detail/39908")

    # | で dict の和が取れる！
    # all_2022 = scrapingColorsFromKeyakiFes("https://sakurazaka46.com/s/s46/diary/detail/44749?ima=0000&link=ROBO004&cd=wkf2022_cont") \
    #     | scrapingColorsFromKeyakiFes("https://www.hinatazaka46.com/s/official/diary/detail/44750?ima=0000&link=ROBO004&cd=wkf2022_cont")

    # サイリウム変えた人確認。
    # for name, colors in all_2021.items():
    #     new_colors = all_2022.get(name)
    #     if not new_colors:
    #         continue

    #     changed = False
    #     for color in colors:
    #         if changed:
    #             continue

    #         if color not in new_colors:
    #             print("\nカラー変わったぞ！")
    #             print(f"========== name {name} =========")
    #             print(f"2021: {colors}")
    #             print(f"2022: {new_colors}")
    #             changed = True

    # # latest
    # all = all_2021
    # for name, colors in all_2022.items():
    #     # 新しいもので上書きしたらいい
    #     all[name] = colors
