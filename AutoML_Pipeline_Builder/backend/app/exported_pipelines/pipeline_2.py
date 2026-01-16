
# Auto-generated ML Pipeline
# Problem type: classification
# Selected model: LogisticRegression
# Metric: 1.0

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, r2_score
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

df = pd.read_csv("uploads/student_performance.csv")

X = pd.get_dummies(df.drop(columns=["pass"]), drop_first=True)
y = df["pass"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

if "classification" == "classification":
    model = LogisticRegression(max_iter=1000) if "LogisticRegression" == "LogisticRegression" else RandomForestClassifier()
    scorer = accuracy_score
else:
    model = LinearRegression() if "LogisticRegression" == "LinearRegression" else RandomForestRegressor()
    scorer = r2_score

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", model)
])

pipeline.fit(X_train, y_train)
score = scorer(y_test, pipeline.predict(X_test))

print("Final score:", score)
