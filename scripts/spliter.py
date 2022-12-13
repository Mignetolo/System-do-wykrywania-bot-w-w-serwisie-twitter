import os
import json
######USE ONLY ONCE

bots = 1386
humans = 4182


def dump(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


for filename in os.listdir("data/dataset_raw_json"):
    with open(f'data/dataset_raw_json/{filename}') as f:
        data = json.load(f)
        print(f'{filename} {data["bool"]}')
    if bots == 0 and humans == 0:
        dump(f'data/data_aftersplit_users/{filename}', data)
    if data["bool"] == "human":
       if humans > 0:
           humans -= 1
       else:
           dump(f'data/data_aftersplit_users/{filename}', data)
           continue
    else:
        if bots > 0:
            bots -= 1
        else:
            dump(f'data/data_aftersplit_users/{filename}', data)
            continue
    with open(f'data/data_aftersplit_text/{filename}', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
