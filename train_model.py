import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


# ------------------------------------------------
# LOAD DATASET
# ------------------------------------------------

data = pd.read_csv("dataset.csv")

X = data["question"]


# ------------------------------------------------
# CONVERT MULTIPLE INTENTS
# ------------------------------------------------

intent_lists = data["intent"].apply(
    lambda x: x.split("|")
)


# ------------------------------------------------
# CONVERT INTENTS INTO BINARY LABELS
# ------------------------------------------------

mlb = MultiLabelBinarizer()

y = mlb.fit_transform(intent_lists)


# ------------------------------------------------
# CREATE ML MODEL
# ------------------------------------------------

model = Pipeline([

    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),

    (
        "classifier",
        OneVsRestClassifier(
            LogisticRegression(
                max_iter=2000
            )
        )
    )

])


# ------------------------------------------------
# TRAIN MODEL
# ------------------------------------------------

model.fit(X, y)


# ------------------------------------------------
# SAVE MODEL + LABEL ENCODER
# ------------------------------------------------

with open("model.pkl", "wb") as file:

    pickle.dump(
        {
            "model": model,
            "mlb": mlb
        },
        file
    )


# ------------------------------------------------
# SUCCESS MESSAGE
# ------------------------------------------------

print("======================================")
print("Multi-Intent Model Trained Successfully")
print("======================================")

print("Available Intents:")

for intent in mlb.classes_:

    print("-", intent)

print("======================================")
print("Model saved as model.pkl")
print("======================================")