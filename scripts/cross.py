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
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.pipeline import make_pipeline
import lime.lime_tabular
import os
from html2image import Html2Image
import lime
from sklearn.model_selection import cross_val_score

def cross_text():
    df = pd.read_excel("data\data_text_clean2.xls")
    X = df["text"].values.astype(str)
    Y = df["bot"].replace({'bot': 1, 'human': 0})
    TT = TweetTokenizer(strip_handles=True, reduce_len=True)
    tfidf = TfidfVectorizer(max_features=10000, ngram_range=(
        1, 2), tokenizer=(TT.tokenize))
    models = [MultinomialNB(), RandomForestClassifier()]
    for model in models:
        pipe = make_pipeline(tfidf, model)
        scores = cross_val_score(pipe, X, Y, cv=5)
        with open(f"models/text/{str(model)[0:-2]}_cross_performance.txt", 'w') as f:
            f.write(str(scores))
            
def cross_user():
    df = pd.read_excel("data\data_users_MultinomialNB.xls")
    X = df.drop(["bool", "name"], axis=1).to_numpy()
    Y = df["bool"].replace({'bot': 1, 'human': 0})
    models = [MultinomialNB(), RandomForestClassifier()]
    for model in models:
        pipe = make_pipeline(model)
        scores = cross_val_score(pipe, X, Y, cv=5)
        with open(f"models/users/{str(model)[0:-2]}_cross_performance.txt", 'w') as f:
            f.write(str(scores))
            
            
cross_text()
cross_user()