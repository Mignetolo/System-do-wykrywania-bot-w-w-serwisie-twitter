import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
from spellchecker import SpellChecker

df2 = pd.read_excel("data/data_text.xls")
df = df2
df = df["text"].astype(str)
df = df.str.lower()


def remove_misspell(text):
    corrected_text = []
    misspelled = SpellChecker().unknown(text.split())
    tic = time.perf_counter()
    for word in text.split():
        if word in misspelled:
            corrected_text.append(SpellChecker().correction(word))
        else:
            corrected_text.append(word)
    print(time.perf_counter() - tic)
    return " ".join(word for word in corrected_text if word is not None)


STOPWORDS = stopwords.words('english')
custom_stopwords = ["rt", "us", "im", "i’m", "it’s"]
for item in custom_stopwords:
    STOPWORDS.append(item)


def remove_punctuatuion(text):
    return text.translate(str.maketrans('', '', string.punctuation))


def remove_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])


def remove_url(text):
    url_pattern = re.compile(
        r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')
    return url_pattern.sub(r'', text)


def lemmatizer(text):
    return " ".join([WordNetLemmatizer().lemmatize(word) for word in text.split()])


def cleaner(X):
    X = X.astype(str)
    X = X.str.lower()
    X = X.apply(lambda text: remove_punctuatuion(text))
    X = X.apply(lambda text: remove_url(text))
    X = X.apply(lambda text: remove_stopwords(text))
    #df = df.apply(lambda text: remove_misspell(text))
    X = X.apply(lambda text: lemmatizer(text))