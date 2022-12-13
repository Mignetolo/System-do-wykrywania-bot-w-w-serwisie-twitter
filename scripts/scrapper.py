import json
import requests
import pandas as pd
from requests.structures import CaseInsensitiveDict
import time


def req(url):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers[
        "Authorization"
    ] = (
        "Bearer "
        + "" #tutaj należy umieścić klucz prywatny
    )
    return (requests.get(url, headers=headers)).json()


def get_user(id):
    url = (
        "https://api.twitter.com/2/users/"
        + id
        + "?user.fields=public_metrics,created_at,profile_image_url,description,location,verified"
    )
    return (req(url))


def get_tweets(id):
    url = (
        "https://api.twitter.com/2/users/"
        + id
        + "/tweets?max_results=6&tweet.fields=created_at,public_metrics,attachments&="
    )
    return (req(url))


def read_json(filename):
    return json.load(open(filename))


bots = 0
deleted = 0
dataset = pd.read_csv('twitter_human_bots_dataset.csv')
for index, id in enumerate(dataset.iloc, start=1):
    try:
        count = 0
        while True:
            data = get_user(str(id[0]))
            if data["status"] == 429:
                print(f"timeout {count}")
                count += 1
                time.sleep(30)
    except:
        pass
    try:
        data = get_user(str(id[0]))
        data = data["data"]
        data["tweets"] = get_tweets(str(id[0]))["data"]
        data["bool"] = str(id[1])
        with open(f'{index-deleted}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        if id[1] == 'bot':
            bots += 1
            print(f'{bots}/{index-deleted}')
    except Exception as e:
        print(f'{index} {id[0]} {id[1]} {e}')
        deleted += 1
print(f' {deleted} usuniętych | {bots} botów | {index-deleted} dobrych')
