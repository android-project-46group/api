import json


# 詳細情報とブログURLを結合する
def main():
    with open("./detailed.json", mode="r", encoding='utf-8') as f:
        x = json.load(f)
    print(x)
    with open("./blogUrls.txt", mode="r", encoding='utf-8') as f:
        blogs = json.load(f)
    converted = []
    for k, v in x.items():
        item = {}
        print(k)
        print(v)
        item["name_ja"] = v["name_ja"]
        bd = v["birthday"].split("/")
        item["birthday"] = f"{bd[0]}年{bd[1]}月{bd[2]}日"
        item["height"] = v["height"]
        item["blood_type"] = v["blood_type"]
        item["generation"] = v["generation"]
        print(k)
        if item["generation"] == "5期生":
            item["blog_url"] = blogs["5期生リレー"]
        elif v["graduation"] == "NO":
            item["blog_url"] = blogs[k]
        else:
            # 公式ブログトップ
            item["blog_url"] = "https://www.nogizaka46.com/s/n46/diary/MEMBER?ima=5830"
        item["img_url"] = v["img_url"].replace(" ", "")

        converted.append(item)
    print(converted)
    with open("./converted.json", mode="w", encoding="utf-8") as f:
        json.dump(converted, f, indent=2)

main()
