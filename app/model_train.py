# model_train.py
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import pandas as pd

def train_and_save(path='model.joblib'):
    data = load_breast_cancer(as_frame=True)
    X = data.frame.drop(columns=['target'])
    y = data.frame['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    print("Classification report:\n", classification_report(y_test, preds))
    joblib.dump({'model': clf, 'columns': X.columns.tolist()}, path)
    print(f"Saved model to {path}")

if __name__ == "__main__":
    train_and_save()
