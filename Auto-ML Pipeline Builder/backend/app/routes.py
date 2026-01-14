from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

from .services import (
    create_pipeline,
    list_pipelines,
    get_pipeline,
    execute_pipeline_async,
)

router = APIRouter()

# -----------------------------
# Dataset storage directory
# -----------------------------
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# -----------------------------
# Upload dataset (CSV)
# -----------------------------
@router.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    save_path = DATA_DIR / file.filename

    with open(save_path, "wb") as f:
        f.write(await file.read())

    return {
        "dataset_name": file.filename
    }

# -----------------------------
# Create pipeline
# -----------------------------
@router.post("/pipeline")
def create_pipeline_route(config: dict):
    """
    Expected config:
    {
      "dataset_name": "file.csv",
      "target_column": "target"
    }
    """
    if "dataset_name" not in config or "target_column" not in config:
        raise HTTPException(
            status_code=400,
            detail="dataset_name and target_column are required",
        )

    return create_pipeline(config)

# -----------------------------
# List pipelines
# -----------------------------
@router.get("/pipelines")
def list_pipelines_route():
    return list_pipelines()

# -----------------------------
# Get pipeline details
# -----------------------------
@router.get("/pipeline/{pipeline_id}")
def get_pipeline_route(pipeline_id: int):
    pipeline = get_pipeline(pipeline_id)
    if pipeline is None:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline

# -----------------------------
# Execute pipeline
# -----------------------------
@router.post("/pipeline/{pipeline_id}/execute")
def execute_pipeline_route(pipeline_id: int):
    pipeline = get_pipeline(pipeline_id)
    if pipeline is None:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    execute_pipeline_async(pipeline_id)
    return {"status": "started"}