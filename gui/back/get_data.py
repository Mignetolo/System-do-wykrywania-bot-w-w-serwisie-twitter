import requests
import pandas as pd
from requests.structures import CaseInsensitiveDict
import pickle
import os
from .text_model import text_prediction_explain

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


def get_user_data(id, model, explain):
    pipe = pickle.load(
        open(f"models/text/{model}", 'rb'), encoding='bytes')
    features_user = ["username", "verified", "description", "public_metrics"]
    public_metrics_tweet = ["retweet_count",
                            "reply_count", "like_count", "quote_count"]
    public_metrics_user = ["followers_count",
                           "following_count", "tweet_count", "listed_count"]
    features_tweet = ["text", "public_metrics"]
    id = str(id)
    data = get_user(id)["data"]
    print(get_tweets(id))
    data["tweets"] = get_tweets(id)["data"]
    data2 = {}
    data_text = []
    for feature in features_user:
        if feature == "public_metrics":
            for metric in public_metrics_user:
                key = metric
                value = data[feature][metric]
        elif feature == "description":
            key = feature
            value = pipe.predict_proba([str(data[feature])])[0][0]
        else:
            key = feature
            value = data[feature]
        data2[key] = value
    average_likes, average_retweet, average_replies, average_quote = 0, 0, 0, 0
    for id, tweets in enumerate(data["tweets"]):
        average_likes += tweets["public_metrics"]["like_count"]
        average_retweet += tweets["public_metrics"]["retweet_count"]
        average_replies += tweets["public_metrics"]["reply_count"]
        average_quote += tweets["public_metrics"]["quote_count"]
        data_text.append(tweets["text"])
    data2["average_likes"] = average_likes/len(data["tweets"])
    data2["average_retweet"] = average_retweet/len(data["tweets"])
    data2["average_replies"] = average_replies/len(data["tweets"])
    data2["average_quote"] = average_quote/len(data["tweets"])
    print(data_text)
    average_value = text_prediction_explain(data_text, model, explain)
    print(average_value)
    data2["tweets score"] = average_value
    df = pd.json_normalize(data2)
    return df


def get_follow(id, followersORFollowing="followers"):
    url = (
        "https://api.twitter.com/2/users/"
        + str(id)
        + "/"
        + followersORFollowing
    )
    return (req(url)["data"])

def id_from_username(username):
    url = (
        "https://api.twitter.com/2/users/by/username/"
        + str(username)
    )
    return (req(url)["data"]["id"])
