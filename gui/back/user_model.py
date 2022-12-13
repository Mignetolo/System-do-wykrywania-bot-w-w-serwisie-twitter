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
from .get_data import get_user_data
import lime


def train(datapath):
    df = pd.read_excel(datapath)
    print(df)
    X = df.drop(["bool", "name"], axis=1).to_numpy()
    Y = df["bool"].replace({'bot': 1, 'human': 0})
    X_train, X_test, Y_train, Y_test = train_test_split(
            X, Y, test_size=0.2, random_state=0)
    models = [MultinomialNB(), RandomForestClassifier()]
    for model in models:
        pipe = make_pipeline(model)
        pipe.fit(X_train, Y_train)
        pickle.dump(pipe, open(f"models/users/{str(model)[0:-2]}", 'wb'))
        with open(f"models/users/{str(model)[0:-2]}_performance.txt", 'w') as f:
            f.write(classification_report(Y_test, pipe.predict(X_test)))

def user_prediction(id, user_model, text_model):
    data = get_user_data(id, text_model)
    data = data.drop("username", axis=1)
    pipe = pickle.load(
        open(f"models/users/MB/{user_model}", 'rb'), encoding='bytes')
    return pipe.predict(data)

def user_prediction_explain(id, user_model, text_model, explain=True):
    data = get_user_data(id, text_model, explain)
    data = data.drop("username", axis=1)
    pipe = pickle.load(
        open(f"models/users/MB/{user_model}", 'rb'), encoding='bytes')
    if explain is True:
        X_train = pd.read_excel("data/data_users_MultinomialNB.xls").drop(
                ["name", "bool"], axis=1).astype(float)
        class_names = ['human', 'bot']
        explainer = lime.lime_tabular.LimeTabularExplainer(
            X_train.to_numpy(), feature_names=pipe.feature_names_in_, class_names=["human", "bot"], discretize_continuous=True)
        exp = explainer.explain_instance(
            data.to_numpy()[0], pipe.predict_proba, num_features=8)
        exp.save_to_file('oi.html')
        hti = Html2Image()
        hti.output_path = 'gui/temp'
        hti.screenshot(
            html_file='oi.html',
            save_as=f'account.png',
            size=(1000, 300)
        )
        os.remove('oi.html')
    return(pipe.predict(data))    