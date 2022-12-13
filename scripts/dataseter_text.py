import json
import pandas as pd
import os


df2 = pd.DataFrame()
for filename in os.listdir("data/data_aftersplit_text"):
    with open(f'data/data_aftersplit_text/{filename}') as f:
        data = json.load(f)
    for tweet in data["tweets"]:
        data2 = {}
        data2["bot"] = data["bool"]
        data2["text"] = tweet["text"]
        df = pd.json_normalize(data2)
        df2 = pd.concat([df2, df])
    data2 = {}
    data2["text"] = data["description"]
    data2["bot"] = data["bool"]
df2.to_excel('data_text.xls', sheet_name='Sheet1',
             index=False, engine='xlsxwriter')
