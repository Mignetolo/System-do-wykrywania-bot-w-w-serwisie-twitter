import json
import pandas as pd
import os
import pickle
public_metrics_user = ["followers_count",
                       "following_count", "tweet_count", "listed_count"]
features_user = ["name", "verified", "description",
                 "public_metrics", "bool"]
public_metrics_tweet = ["retweet_count",
                        "reply_count", "like_count", "quote_count"]
features_tweet = ["text", "public_metrics"]
flaga = 0
df2 = pd.DataFrame()
filenames = os.listdir("data/data_aftersplit_users")
filenames_len = len(os.listdir("data/data_aftersplit_users"))
models = ["MultinomialNB", "RandomForestClassifier"]
for model in models:
    pipe = pickle.load(
        open(f"models/text/{model}", 'rb'), encoding='bytes')
    for id, filename in enumerate(filenames):
        print(f"{id} / {filenames_len}")
        with open(f'data/data_aftersplit_users/{filename}') as f:
            data = json.load(f)
        data2 = {}
        data3 = {}
        for feature in features_user:
            if feature == "public_metrics":
                for metric in public_metrics_user:
                    key = metric
                    value = data[feature][metric]
            elif feature == "description":
                key = feature
                value = pipe.predict_proba([str(data[feature])])[0][0]
                print(value)
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
            data3[f'text {id}'] = tweets["text"]
        data2["average_likes"] = average_likes/len(data["tweets"])
        data2["average_retweet"] = average_retweet/len(data["tweets"])
        data2["average_replies"] = average_replies/len(data["tweets"])
        data2["average_quote"] = average_quote/len(data["tweets"])
        df3 = pd.json_normalize(data3)
        average_value = 0
        values = pipe.predict_proba(df3.iloc[0])
        for item in values:
            average_value += item[0]
        average_value /= len(values)
        data2["tweets score"] = average_value
        df = pd.json_normalize(data2)
        df2 = pd.concat([df2, df])
    df2.to_excel(f'data/data_users_{model}.xls', sheet_name='Sheet1',
                 index=False, engine='xlsxwriter')
