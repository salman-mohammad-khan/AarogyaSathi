import json

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from app.config import TRAINING_DIR

_data = None
_vectorizer = None
_classifier = None
_intent_names = None


def load():
    global _data, _vectorizer, _classifier, _intent_names
    with open(TRAINING_DIR / "intents.json", encoding="utf-8") as f:
        _data = json.load(f)
    examples, labels = [], []
    for intent, texts in _data["intents"].items():
        for text in texts:
            examples.append(text.lower())
            labels.append(intent)
    _vectorizer = TfidfVectorizer(
        analyzer="char_wb", ngram_range=(2, 5), max_features=30000, sublinear_tf=True
    )
    X = _vectorizer.fit_transform(examples)
    _classifier = LogisticRegression(C=8.0, max_iter=1000, solver="lbfgs")
    _classifier.fit(X, labels)
    _intent_names = sorted(set(labels))


def predict_intent(text, threshold=0.5):
    if _classifier is None:
        load()
    X = _vectorizer.transform([text.lower()])
    probs = _classifier.predict_proba(X)[0]
    order = np.argsort(probs)[::-1]
    best = _classifier.classes_[order[0]]
    conf = float(probs[order[0]])
    if conf < threshold:
        return None, conf
    return best, conf


def predict_intent_scores(text):
    if _classifier is None:
        load()
    X = _vectorizer.transform([text.lower()])
    probs = _classifier.predict_proba(X)[0]
    return {
        cls: float(p) for cls, p in sorted(zip(_classifier.classes_, probs), key=lambda kv: kv[1], reverse=True)
    }
