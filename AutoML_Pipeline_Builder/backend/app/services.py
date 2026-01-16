import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, r2_score
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# ----------------------------
# In-memory pipeline registry
# ----------------------------
PIPELINES = []
PIPELINE_ID = 1

BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "exported_pipelines"
EXPORT_DIR.mkdir(exist_ok=True)

# ----------------------------
# Pipeline creation
# ----------------------------
def create_pipeline(dataset_path: str, target_column: str):
    global PIPELINE_ID

    df = pd.read_csv(dataset_path)

    problem_type, best_model, best_score = select_best_model(df, target_column)

    pipeline = {
        "id": PIPELINE_ID,
        "dataset_path": dataset_path,
        "target_column": target_column,
        "problem_type": problem_type,
        "model": best_model,
        "metric": best_score,
        "status": "created",
    }

    PIPELINES.append(pipeline)
    PIPELINE_ID += 1

    generate_pipeline_py(
        pipeline_id=pipeline["id"],
        dataset_path=dataset_path,
        target_column=target_column,
        problem_type=problem_type,
        selected_model=best_model,
        metric=best_score,
    )

    return pipeline

# ----------------------------
# List pipelines
# ----------------------------
def list_pipelines():
    return PIPELINES

# ----------------------------
# Run pipeline (optional)
# ----------------------------
def run_pipeline(pipeline_id: int):
    pipeline = next(p for p in PIPELINES if p["id"] == pipeline_id)

    df = pd.read_csv(pipeline["dataset_path"])
    X = pd.get_dummies(df.drop(columns=[pipeline["target_column"]]), drop_first=True)
    y = df[pipeline["target_column"]]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    if pipeline["problem_type"] == "classification":
        model = (
            LogisticRegression(max_iter=1000)
            if pipeline["model"] == "LogisticRegression"
            else RandomForestClassifier()
        )
        scorer = accuracy_score
    else:
        model = (
            LinearRegression()
            if pipeline["model"] == "LinearRegression"
            else RandomForestRegressor()
        )
        scorer = r2_score

    model.fit(X_train, y_train)
    pipeline["metric"] = scorer(y_test, model.predict(X_test))
    pipeline["status"] = "completed"

    return pipeline

# ----------------------------
# Model selection
# ----------------------------
def select_best_model(df, target_column):
    X = pd.get_dummies(df.drop(columns=[target_column]), drop_first=True)
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    if y.dtype == "object" or y.nunique() <= 20:
        problem_type = "classification"
        models = {
            "LogisticRegression": LogisticRegression(max_iter=1000),
            "RandomForestClassifier": RandomForestClassifier(),
        }
        scorer = accuracy_score
    else:
        problem_type = "regression"
        models = {
            "LinearRegression": LinearRegression(),
            "RandomForestRegressor": RandomForestRegressor(),
        }
        scorer = r2_score

    best_score = float("-inf")
    best_model_name = None

    for name, model in models.items():
        pipe = Pipeline([
            ("scaler", StandardScaler()),
            ("model", model),
        ])
        pipe.fit(X_train, y_train)
        score = scorer(y_test, pipe.predict(X_test))

        if score > best_score:
            best_score = score
            best_model_name = name

    return problem_type, best_model_name, best_score

# ----------------------------
# Generate downloadable pipeline
# ----------------------------
def generate_pipeline_py(
    pipeline_id: int,
    dataset_path: str,
    target_column: str,
    problem_type: str,
    selected_model: str,
    metric: float,
):
    code = f'''
# Auto-generated ML Pipeline
# Problem type: {problem_type}
# Selected model: {selected_model}
# Metric: {metric}

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, r2_score
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

df = pd.read_csv("{dataset_path}")

X = pd.get_dummies(df.drop(columns=["{target_column}"]), drop_first=True)
y = df["{target_column}"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

if "{problem_type}" == "classification":
    model = LogisticRegression(max_iter=1000) if "{selected_model}" == "LogisticRegression" else RandomForestClassifier()
    scorer = accuracy_score
else:
    model = LinearRegression() if "{selected_model}" == "LinearRegression" else RandomForestRegressor()
    scorer = r2_score

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", model)
])

pipeline.fit(X_train, y_train)
score = scorer(y_test, pipeline.predict(X_test))

print("Final score:", score)
'''

    output_file = EXPORT_DIR / f"pipeline_{pipeline_id}.py"
    output_file.write_text(code)

    return output_file