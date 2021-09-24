from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials

# JSONのパス (XXXXX, YYYYY は任意の文字列)
JSON_PATH = 'serviceAccountKey.json'

# 初期化
cred = credentials.Certificate(JSON_PATH)
firebase_admin.initialize_app(cred)

db = firestore.client()


GROUP_NAME = "nogizaka"

# Json のデータを、DB に保存する！
DATA_PATH = f'../scraping/{GROUP_NAME}/detailed_infos.txt'

# データの保存
# データ例
# "akimotomanatsu": {
#     "名前": "秋元 真夏",
#     "生年月日": "1993年8月20日",
#     "血液型": "B型",
#     "星座": "しし座",
#     "身長": "154cm",
# },
def save_info():

    print(DATA_PATH)
    import json
    # member_infos = ""
    with open(DATA_PATH, mode='rt', encoding='utf-8') as f:
        member_infos = json.load(f)

    for name_en, member_info in member_infos.items():
        print(name_en)
        print(member_info["生年月日"])

        doc_ref = db.collection(f'{GROUP_NAME}').document(f'{name_en}')
        doc_ref.set({
            u'name_en': name_en,
            u'name_ja': member_info["名前"],
            u'birthday': member_info["生年月日"],
            u'height': member_info["身長"]
        })

def save_urls():
    import json
    # member_infos = ""
    with open(f"url_infos_{GROUP_NAME}.txt", mode='rt', encoding='utf-8') as f:
        url_infos = json.load(f)

    for name_en, url in url_infos.items():
        print(name_en)
        print(url)

        doc_ref = db.collection(f'{GROUP_NAME}').document(f'{name_en}')
        doc_ref.set({
            u'img_url': url
        })

def main():

    import json
    # member_infos = ""
    with open(f"url_infos_{GROUP_NAME}.txt", mode='rt', encoding='utf-8') as f:
        url_infos = json.load(f)

    print(DATA_PATH)
    import json
    # member_infos = ""
    with open(DATA_PATH, mode='rt', encoding='utf-8') as f:
        member_infos = json.load(f)

    for name_en, member_info in member_infos.items():
        print(name_en)
        print(member_info["生年月日"])

        doc_ref = db.collection(f'{GROUP_NAME}').document(f'{name_en}')
        doc_ref.set({
            u'name_en': name_en,
            u'name_ja': member_info["名前"],
            u'birthday': member_info["生年月日"],
            u'height': member_info["身長"],
            u'img_url': url_infos[name_en]
        })

if __name__ == "__main__":
    main()
    # save_urls()
