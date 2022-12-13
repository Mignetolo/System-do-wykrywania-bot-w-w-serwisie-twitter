import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from nltk.tokenize import TweetTokenizer
import pickle
from sklearn.pipeline import make_pipeline
from lime.lime_text import LimeTextExplainer
import os
from html2image import Html2Image


def train(datapath):
    df = pd.read_excel(datapath)
    X = df["text"].values.astype(str)
    Y = df["bot"].replace({'bot': 1, 'human': 0})
    TT = TweetTokenizer(strip_handles=True, reduce_len=True)
    tfidf = TfidfVectorizer(max_features=10000, ngram_range=(
        1, 2), tokenizer=(TT.tokenize))
    X_train, X_test, Y_train, Y_test = train_test_split(
            X, Y, test_size=0.2, random_state=0)
    models = [MultinomialNB(), RandomForestClassifier()]
    for model in models:
        pipe = make_pipeline(tfidf, model)
        pipe.fit(X_train, Y_train)
        pickle.dump(pipe, open(f"models/text/{str(model)[0:-2]}", 'wb'))
        with open(f"models/text/{str(model)[0:-2]}_performance.txt", 'w') as f:
            f.write(classification_report(Y_test, pipe.predict(X_test)))


def text_prediction_explain(tweets_text, model, explain=True):
    pipe = pickle.load(
        open(f"models/text/{model}", 'rb'), encoding='bytes')
    print(pipe.get_params())
    average_value = 0
    if explain is True:
        for filename in os.listdir("gui/temp"):
                os.remove(f"gui/temp/{filename}")
        for id,tweet_text in enumerate(tweets_text):
            hti = Html2Image()
            print(tweet_text)
            class_names = ['human', 'bot']
            explainer = LimeTextExplainer(class_names=class_names)
            exp = explainer.explain_instance(
                    tweet_text, pipe.predict_proba)
            exp.save_to_file('oi.html')
            hti.output_path = 'gui/temp'
            hti.screenshot(
                        html_file='oi.html',
                        save_as=f'tweet {id+1}.png',
                        size=(1000, 300)
                    )
            os.remove('oi.html')
            average_value += pipe.predict_proba([tweet_text])[0][0]
    else:
        for tweet_text in tweets_text:
            average_value += pipe.predict_proba([tweet_text])[0][0]
    print(f"test {average_value}")
    return average_value/len(tweets_text)