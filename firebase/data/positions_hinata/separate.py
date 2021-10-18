import json


def main(json_load):
    songs = {}

    with open(f'data/positions_hinata/songs.json', 'w') as f:
        json.dump(formation_infos, f, indent=2)


if __name__ == '__main__':
    json_open = open('position_all.json', 'r')
    json_load = json.load(json_open)    # Top がリストだああ
    # for item in json_load:
    #     print(type(item))
    main(json_load)
    for k, v in json_load[0].items():
        print(k)
        print(v)
    # res = main(json_load)
    # print(res)
