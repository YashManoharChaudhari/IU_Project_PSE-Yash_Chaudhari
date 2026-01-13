import logging
from pathlib import Path
from .models import pipelines

DATA_DIR = Path(__file__).parent.parent / "data"
ARTIFACT_DIR = Path(__file__).parent.parent / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)

def create_pipeline(config: dict):
    pipeline_id = len(pipelines) + 1
    pipelines[pipeline_id] = {
        "config": config,
        "status": "created",
        "task_type": None,
        "model_name": None,
        "metric": None,
        "metric_name": None,
        "artifacts": None,
    }
    return {"pipeline_id": pipeline_id, "status": "created"}

def list_pipelines():
    return [
        {"pipeline_id": pid, "status": p["status"]}
        for pid, p in pipelines.items()
    ]

def get_pipeline(pipeline_id: int):
    return pipelines.get(pipeline_id, {"error": "Pipeline not found"})

async def execute_pipeline_async(pipeline_id: int):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.metrics import accuracy_score, mean_squared_error
    from sklearn.linear_model import LogisticRegression, LinearRegression
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.svm import SVC, SVR

    pipeline = pipelines.get(pipeline_id)
    if not pipeline:
        return

    try:
        pipeline["status"] = "running"

        dataset_name = Path(pipeline["config"]["dataset_path"]).name
        target = pipeline["config"]["target_column"]
        dataset_path = DATA_DIR / dataset_name

        if not dataset_path.exists():
            raise FileNotFoundError(f"{dataset_path} not found")

        df = pd.read_csv(dataset_path)
        X = pd.get_dummies(df.drop(columns=[target]), drop_first=True)
        y = df[target]

        # Detect task type
        if y.dtype in ["float64", "float32"] and y.nunique() > 20:
            task_type = "regression"
        else:
            task_type = "classification"

        pipeline["task_type"] = task_type

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )

        if task_type == "classification":
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
            metric_fn = accuracy_score
            better = lambda s, b: b is None or s > b
            metric_name = "accuracy"
        else:
            models = {
                "LinearRegression": Pipeline([
                    ("scaler", StandardScaler()),
                    ("model", LinearRegression())
                ]),
                "RandomForestRegressor": RandomForestRegressor(),
                "SupportVectorRegressor": Pipeline([
                    ("scaler", StandardScaler()),
                    ("model", SVR())
                ])
            }
            metric_fn = lambda y, p: mean_squared_error(y, p, squared=False)
            better = lambda s, b: b is None or s < b
            metric_name = "rmse"

        best_score = None
        best_model_name = None

        for name, model in models.items():
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            score = metric_fn(y_test, preds)
            if better(score, best_score):
                best_score = score
                best_model_name = name

        pipeline["model_name"] = best_model_name
        pipeline["metric"] = round(float(best_score), 3)
        pipeline["metric_name"] = metric_name

        model_file = ARTIFACT_DIR / f"model_{pipeline_id}.txt"
        script_file = ARTIFACT_DIR / f"pipeline_{pipeline_id}.py"

        model_file.write_text(
            f"Task: {task_type}\n"
            f"Model: {best_model_name}\n"
            f"{metric_name.upper()}: {pipeline['metric']}"
        )

        script_file.write_text(f'''
# Auto-generated ML pipeline
# Task type: {task_type}
# Selected model: {best_model_name}
# Metric ({metric_name}): {pipeline["metric"]}

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR

DATASET_PATH = "{dataset_name}"
TARGET_COLUMN = "{target}"

# Load dataset
df = pd.read_csv(DATASET_PATH)

X = df.drop(columns=[TARGET_COLUMN])
y = df[TARGET_COLUMN]

X = pd.get_dummies(X, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Build selected model
model_name = "{best_model_name}"

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

if "{task_type}" == "classification":
    metric = accuracy_score(y_test, preds)
    print("Accuracy:", metric)
else:
    metric = mean_squared_error(y_test, preds, squared=False)
    print("RMSE:", metric)
''')

        BASE_URL = "http://localhost:8000"

        pipeline["artifacts"] = {
            "model": f"{BASE_URL}/download/model/{model_file.name}",
            "script": f"{BASE_URL}/download/script/{script_file.name}",
        }

        pipeline["status"] = "completed"

    except Exception:
        logging.exception("Pipeline execution failed")
        pipeline["status"] = "failed"