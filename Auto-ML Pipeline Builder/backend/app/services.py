import threading
import logging
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# ---------------------------------
# In-memory pipeline store
# ---------------------------------
PIPELINES = {}
PIPELINE_COUNTER = 1

# ---------------------------------
# Data & artifact directories
# ---------------------------------
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ARTIFACT_DIR = BASE_DIR / "artifacts"

DATA_DIR.mkdir(exist_ok=True)
ARTIFACT_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO)

# ---------------------------------
# Pipeline CRUD
# ---------------------------------
def create_pipeline(config: dict):
    global PIPELINE_COUNTER

    pipeline_id = PIPELINE_COUNTER
    PIPELINE_COUNTER += 1

    PIPELINES[pipeline_id] = {
        "pipeline_id": pipeline_id,
        "config": config,
        "status": "created",
        "model_name": None,
        "metric": None,
        "artifacts": None,
    }

    return PIPELINES[pipeline_id]


def list_pipelines():
    return list(PIPELINES.values())


def get_pipeline(pipeline_id: int):
    return PIPELINES.get(pipeline_id)


def update_pipeline(pipeline_id: int, **updates):
    if pipeline_id in PIPELINES:
        PIPELINES[pipeline_id].update(updates)


# ---------------------------------
# Pipeline execution
# ---------------------------------
def execute_pipeline_async(pipeline_id: int):
    thread = threading.Thread(
        target=execute_pipeline,
        args=(pipeline_id,),
        daemon=True,
    )
    thread.start()


def execute_pipeline(pipeline_id: int):
    try:
        logging.info(f"Pipeline {pipeline_id} started")
        update_pipeline(pipeline_id, status="running")

        pipeline = get_pipeline(pipeline_id)
        config = pipeline["config"]

        dataset_name = config["dataset_name"]
        target = config["target_column"]

        dataset_path = DATA_DIR / dataset_name
        if not dataset_path.exists():
            raise FileNotFoundError(f"Dataset {dataset_name} not found")

        # -----------------------------
        # Load dataset
        # -----------------------------
        df = pd.read_csv(dataset_path)

        if target not in df.columns:
            raise ValueError(f"Target column '{target}' not found in dataset")

        X = df.drop(columns=[target])
        y = df[target]

        X = pd.get_dummies(X, drop_first=True)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )

        # -----------------------------
        # Decide task type
        # -----------------------------
        is_classification = y.nunique() <= 20 and y.dtype != float

        # -----------------------------
        # Candidate models
        # -----------------------------
        if is_classification:
            models = {
                "LogisticRegression": Pipeline(
                    [
                        ("scaler", StandardScaler()),
                        ("model", LogisticRegression(max_iter=1000)),
                    ]
                ),
                "RandomForestClassifier": RandomForestClassifier(random_state=42),
            }
        else:
            models = {
                "LinearRegression": Pipeline(
                    [
                        ("scaler", StandardScaler()),
                        ("model", LinearRegression()),
                    ]
                ),
                "RandomForestRegressor": RandomForestRegressor(random_state=42),
            }

        best_model_name = None
        best_model = None
        best_metric = None

        # -----------------------------
        # Train & evaluate
        # -----------------------------
        for name, model in models.items():
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            if is_classification:
                metric = accuracy_score(y_test, preds)
            else:
                metric = r2_score(y_test, preds)

            if best_metric is None or metric > best_metric:
                best_metric = metric
                best_model = model
                best_model_name = name

        # -----------------------------
        # Save artifacts
        # -----------------------------
        model_path = ARTIFACT_DIR / f"model_{pipeline_id}.txt"
        pipeline_path = ARTIFACT_DIR / f"pipeline_{pipeline_id}.py"

        model_path.write_text(
            f"Selected model: {best_model_name}\nMetric: {best_metric}"
        )

        pipeline_path.write_text(
            f"""# Auto-generated ML pipeline

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, r2_score
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

DATASET = "{dataset_name}"
TARGET = "{target}"

df = pd.read_csv(DATASET)
X = pd.get_dummies(df.drop(columns=[TARGET]), drop_first=True)
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Selected model: {best_model_name}
"""
        )

        update_pipeline(
            pipeline_id,
            status="completed",
            model_name=best_model_name,
            metric=best_metric,
            artifacts={
                "model": f"/artifacts/model_{pipeline_id}.txt",
                "pipeline": f"/artifacts/pipeline_{pipeline_id}.py",
            },
        )

        logging.info(f"Pipeline {pipeline_id} completed")

    except Exception as e:
        logging.exception("Pipeline execution failed")
        update_pipeline(pipeline_id, status="failed")