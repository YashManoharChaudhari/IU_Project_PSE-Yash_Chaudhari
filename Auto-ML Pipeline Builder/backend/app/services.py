import pandas as pd
import threading
from pathlib import Path
from fastapi.responses import FileResponse
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

DATA_DIR = Path("backend/data")
ARTIFACT_DIR = Path("backend/app/artifacts")
DATA_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

PIPELINES = {}
PIPELINE_ID = 1

def save_dataset(file):
    path = DATA_DIR / file.filename
    with open(path, "wb") as f:
        f.write(file.file.read())
    return {"dataset_path": str(path)}

def create_pipeline(req):
    global PIPELINE_ID
    pipeline = {
        "id": PIPELINE_ID,
        "dataset_path": req.dataset_path,
        "target": req.target_column,
        "status": "created",
        "model": None,
        "metric": None,
    }
    PIPELINES[PIPELINE_ID] = pipeline
    PIPELINE_ID += 1
    return pipeline

def execute_pipeline_async(pipeline_id):
    thread = threading.Thread(target=execute_pipeline, args=(pipeline_id,))
    thread.start()

def execute_pipeline(pipeline_id):
    pipeline = PIPELINES[pipeline_id]
    df = pd.read_csv(pipeline["dataset_path"])

    target = pipeline["target"]
    X = pd.get_dummies(df.drop(columns=[target]), drop_first=True)
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # Auto detect task type
    is_regression = y.dtype != "object" and y.nunique() > 10

    if is_regression:
        models = {
            "LinearRegression": LinearRegression(),
            "RandomForestRegressor": RandomForestRegressor(),
        }
        best_score = float("inf")
        metric_name = "mse"
    else:
        models = {
            "LogisticRegression": LogisticRegression(max_iter=1000),
            "RandomForestClassifier": RandomForestClassifier(),
        }
        best_score = 0
        metric_name = "accuracy"

    best_model = None

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        score = (
            mean_squared_error(y_test, preds)
            if is_regression
            else accuracy_score(y_test, preds)
        )

        if (is_regression and score < best_score) or (
            not is_regression and score > best_score
        ):
            best_score = score
            best_model = name

    pipeline["model"] = best_model
    pipeline["metric"] = {metric_name: round(best_score, 4)}
    pipeline["status"] = "completed"

    generate_pipeline_script(pipeline)

def generate_pipeline_script(pipeline):
    script = ARTIFACT_DIR / f"pipeline_{pipeline['id']}.py"

    script.write_text(
        f"""
# Auto-generated ML pipeline
# Model: {pipeline['model']}
# Metric: {pipeline['metric']}

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

df = pd.read_csv("{pipeline['dataset_path']}")

X = pd.get_dummies(df.drop("{pipeline['target']}", axis=1), drop_first=True)
y = df["{pipeline['target']}"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

print("Ready to train {pipeline['model']}")
"""
    )

def list_pipelines():
    return list(PIPELINES.values())

def get_pipeline(pipeline_id):
    return PIPELINES.get(pipeline_id)

def download_pipeline_script(pipeline_id):
    path = ARTIFACT_DIR / f"pipeline_{pipeline_id}.py"
    return FileResponse(path, filename=path.name)