
# Auto-generated ML pipeline
# Task type: classification
# Selected model: LogisticRegression
# Metric (accuracy): 1.0

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR

DATASET_PATH = "loan_default.csv"
TARGET_COLUMN = "default"

# Load dataset
df = pd.read_csv(DATASET_PATH)

X = df.drop(columns=[TARGET_COLUMN])
y = df[TARGET_COLUMN]

X = pd.get_dummies(X, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Build selected model
model_name = "LogisticRegression"

if model_name == "LogisticRegression":
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000))
    ])
elif model_name == "RandomForestClassifier":
    model = RandomForestClassifier(random_state=42)
elif model_name == "SupportVectorMachine":
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("model", SVC())
    ])
elif model_name == "LinearRegression":
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression())
    ])
elif model_name == "RandomForestRegressor":
    model = RandomForestRegressor(random_state=42)
else:
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("model", SVR())
    ])

model.fit(X_train, y_train)
preds = model.predict(X_test)

if "classification" == "classification":
    metric = accuracy_score(y_test, preds)
    print("Accuracy:", metric)
else:
    metric = mean_squared_error(y_test, preds, squared=False)
    print("RMSE:", metric)
