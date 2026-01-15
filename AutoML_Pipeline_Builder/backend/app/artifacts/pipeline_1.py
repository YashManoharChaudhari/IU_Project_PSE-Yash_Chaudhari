
# Auto-generated ML pipeline script

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

DATASET_PATH = "data/sample.csv"
TARGET_COLUMN = "label"

data = pd.read_csv(DATASET_PATH)
X = data.drop(TARGET_COLUMN, axis=1)
y = data[TARGET_COLUMN]

X_train, X_test, y_train, y_test = train_test_split(X, y)

model = RandomForestClassifier()
model.fit(X_train, y_train)
