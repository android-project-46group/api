import json


def main():
    with open("./detailed_infos.txt", mode="r", encoding='utf-8') as f:
        x = json.load(f)
    print(x)
    with open("./blogUrls.txt", mode="r", encoding='utf-8') as f:
        blogs = json.load(f)
    converted = []
    for k, v in x.items():
        item = {}
        item["name_ja"] = v["名前"]
        item["birthday"] = v["生年月日"]
        item["height"] = v["身長"]
        item["blood_type"] = v["血液型"]
        item["generation"] = v["generation"]
        print(k)
        if item["generation"] == "4期生":
            item["blog_url"] = "https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct=2000"
        else:
            item["blog_url"] = blogs[k]
        item["img_url"] = f"https://kokoichi0206.mydns.jp/imgs/hinata/{k}.jpeg"

        converted.append(item)
    print(converted)
    with open("./converted.json", mode="w", encoding="utf-8") as f:
        json.dump(converted, f, indent=2)

main()
