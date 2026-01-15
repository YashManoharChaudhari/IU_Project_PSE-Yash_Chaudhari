
# Auto-generated ML pipeline

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

df = pd.read_csv("data/customer_churn.csv")
X = df.drop("churn", axis=1)
y = df["churn"]

X = pd.get_dummies(X, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

models = {
    "LogisticRegression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000))
    ]),
    "RandomForestClassifier": RandomForestClassifier(),
    "SupportVectorMachine": Pipeline([
        ("scaler", StandardScaler()),
        ("model", SVC())
    ])
}

best_acc = 0
best_model = None

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    if acc > best_acc:
        best_acc = acc
        best_model = name

print("Best model:", best_model)
print("Accuracy:", best_acc)
