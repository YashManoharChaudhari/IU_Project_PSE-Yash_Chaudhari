from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import os
import shutil

from app.models import PipelineCreateRequest
from app.services import (
    create_pipeline,
    run_pipeline,
    PIPELINES,
    generate_pipeline_py,
)

router = APIRouter()

# -------------------------------
# Paths & directories
# -------------------------------
UPLOAD_DIR = Path("uploads")
EXPORT_DIR = Path("exported_pipelines")

UPLOAD_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)

# -------------------------------
# Upload dataset
# -------------------------------
@router.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"dataset_path": str(file_path)}

# -------------------------------
# Create pipeline
# -------------------------------
@router.post("/pipeline")
def create_pipeline_route(req: PipelineCreateRequest):
    pipeline = create_pipeline(req.dataset_path, req.target_column)

    # generate downloadable python pipeline
    generate_pipeline_py(
    pipeline_id=pipeline["id"],
    dataset_path=req.dataset_path,
    target_column=req.target_column,
    problem_type=pipeline["problem_type"],
    selected_model=pipeline["model"],
    metric=pipeline["metric"],
)

    return pipeline

# -------------------------------
# List pipelines
# -------------------------------
@router.get("/pipelines")
def list_pipelines():
    return PIPELINES

# -------------------------------
# Execute pipeline
# -------------------------------
@router.post("/pipeline/{pipeline_id}/execute")
def execute_pipeline(pipeline_id: int):
    return run_pipeline(pipeline_id)

# -------------------------------
# Download pipeline as .py
# -------------------------------
from fastapi.responses import FileResponse
from pathlib import Path

@router.get("/pipeline/{pipeline_id}/download")
def download_pipeline(pipeline_id: int):
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / "exported_pipelines" / f"pipeline_{pipeline_id}.py"

    if not file_path.exists():
        return {"error": f"Pipeline file pipeline_{pipeline_id}.py not found"}

    return FileResponse(
        path=file_path,
        media_type="text/x-python",
        filename=f"pipeline_{pipeline_id}.py",
    )