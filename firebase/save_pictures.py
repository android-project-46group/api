from pyasn1_modules.rfc2459 import UniversalString
import pyrebase

"""
save pictures to Firebare Storage and
make url_infos_{groupName}.txt to save to Database
"""

# // Your web app's Firebase configuration
# // For Firebase JS SDK v7.20.0 and later, measurementId is optional
config = {
    "apiKey": "AIzaSyC8BvN_FqUGTq1njRY6mTNEK6fWGkY9Bmk",
    "authDomain": "my-memory-3b3bd.firebaseapp.com",
    "databaseURL": "https://console.firebase.google.com/u/0/project/my-memory-3b3bd/storage/my-memory-3b3bd.appspot.com/files",
    "projectId": "my-memory-3b3bd",
    "storageBucket": "my-memory-3b3bd.appspot.com",
    "serviceAccount": "serviceAccountKey.json"
}

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()

# GROUP_NAME = "nogizaka"
# GROUP_NAME = "hinatazaka"
GROUP_NAME = "sakurazaka"

def uploadPic(path, name):
    # storage.child("saka").child(GROUP_NAME).child(path).put(f"{name}.jpeg")
    storage.child("saka").child(GROUP_NAME).child(f"{name}.jpeg").put(path)
    url = storage.child("saka").child(GROUP_NAME).child(f"{name}.jpeg").get_url(None)
    return url

def main(DIR_NAME, FILENAMES):
    url_infos = {}
    for file_name in FILENAMES:
        path = f"{DIR_NAME}/{file_name}"
        member_name = file_name.split(".")[0]
        url = uploadPic(path, member_name)
        url_infos[member_name] = url
    return url_infos


if __name__ == "__main__":
    import os
    PIC_DIR = f"../scraping/{GROUP_NAME}/pictures"
    files = os.listdir(PIC_DIR)
    url_infos = main(PIC_DIR, files)

    print(url_infos)

    TAB         = '\t'
    NEW_LINE    = '\n'
    DICT_START  = '{'
    DICT_END    = '}'
    with open(f'url_infos_{GROUP_NAME}.txt', mode='w') as f:
        f.write(f'{DICT_START}{NEW_LINE}')
        cnt = 0
        for name_en, url in url_infos.items():
            cnt += 1
            if cnt == len(url_infos):
                f.write(f'{TAB}"{name_en}": "{url}"{NEW_LINE}')
            else:
                f.write(f'{TAB}"{name_en}": "{url}",{NEW_LINE}')
        f.write(f'{DICT_END}{NEW_LINE}')

