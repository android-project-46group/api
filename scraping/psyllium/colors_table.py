import json


# 詳細情報とブログURLを結合する
def main():
    all = {}
    with open("./nogi.json", mode="r", encoding='utf-8') as f:
        x = json.load(f)
        all |= x
    with open("./sakura.json", mode="r", encoding='utf-8') as f:
        x = json.load(f)
        all |= x
    with open("./hinata.json", mode="r", encoding='utf-8') as f:
        x = json.load(f)
        all |= x

    # 重複のないカラー一覧を取得する。
    colors = set()
    for _, cs in all.items():
        c1, c2 = cs
        colors.add(c1)
        colors.add(c2)

    return colors

if __name__ == "__main__":
    colors = main()

    with open(f"./colors", "w") as f:
        f.write("('" + "'),\n('".join(colors) + "')\n")
