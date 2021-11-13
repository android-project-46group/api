# データの例
# データ例
# "akimotomanatsu": {
#     "blog_url": "https://....",
#     "last_blog_img": "https://kokoichi0206.mydns.jp/...",
#     "last_updated_at": "2021/10/08 17:24"
# },

def main(group_name):
    BLOG_URL_PATH = f'../{group_name}/blogUrls.txt'
    BLOG_INFO_PATH = f'./blog_infos_{group_name}.txt'

    import json
    # member_infos = ""
    with open(BLOG_URL_PATH, mode='rt', encoding='utf-8') as f:
        blog_urls = json.load(f)

    with open(BLOG_INFO_PATH, mode='rt', encoding='utf-8') as f:
        blog_infos = json.load(f)

    tmp = []
    for name, blog_url in blog_urls.items():
        blog_info = blog_infos[name]
        print(blog_info)

        tmp.append({
            'name': name,
            'blog_url': blog_url,
            'last_blog_img': blog_info['pic_url'],
            'last_updated_at': blog_info['last_updated_at'],
        })

    with open(f'outputs/{group_name}.json', 'w') as f:
        json.dump(tmp, f, indent=2)


if __name__ == "__main__":
    GROUP_NAMES = ["nogizaka", "hinatazaka", "sakurazaka"]
    for group in GROUP_NAMES:
        main(group)
