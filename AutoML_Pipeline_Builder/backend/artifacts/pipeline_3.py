
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR

DATASET_PATH = "/Users/yashchaudhari/Documents/Project_Software Engineering/IU_Project_PSE-Yash_Chaudhari/Auto-ML Pipeline Builder/backend/data/student_performance.csv"
TARGET_COLUMN = "pass"

df = pd.read_csv(DATASET_PATH)
X = pd.get_dummies(df.drop(TARGET_COLUMN, axis=1), drop_first=True)
y = df[TARGET_COLUMN]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

model_name = "LogisticRegression"

if model_name == "LogisticRegression":
    model = Pipeline([("scaler", StandardScaler()), ("model", LogisticRegression(max_iter=1000))])
elif model_name == "RandomForestClassifier":
    model = RandomForestClassifier()
elif model_name == "SupportVectorMachine":
    model = Pipeline([("scaler", StandardScaler()), ("model", SVC())])
elif model_name == "LinearRegression":
    model = Pipeline([("scaler", StandardScaler()), ("model", LinearRegression())])
elif model_name == "RandomForestRegressor":
    model = RandomForestRegressor()
else:
    model = Pipeline([("scaler", StandardScaler()), ("model", SVR())])

model.fit(X_train, y_train)
preds = model.predict(X_test)

if "classification" == "classification":
    print("Accuracy:", accuracy_score(y_test, preds))
else:
    print("RMSE:", mean_squared_error(y_test, preds, squared=False))
