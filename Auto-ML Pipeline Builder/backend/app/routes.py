from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path
from .services import (
    create_pipeline,
    list_pipelines,
    get_pipeline,
    execute_pipeline_async,
)

router = APIRouter()

ARTIFACT_DIR = Path(__file__).parent.parent / "artifacts"

@router.post("/pipeline")
def create_pipeline_route(config: dict):
    return create_pipeline(config)

@router.get("/pipelines")
def list_pipelines_route():
    return list_pipelines()

@router.get("/pipeline/{pipeline_id}")
def get_pipeline_route(pipeline_id: int):
    return get_pipeline(pipeline_id)

@router.post("/pipeline/{pipeline_id}/execute")
def execute_pipeline_route(pipeline_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(execute_pipeline_async, pipeline_id)
    return {"pipeline_id": pipeline_id, "status": "execution started"}



@router.get("/download/model/{filename}")
def download_model(filename: str):
    file_path = ARTIFACT_DIR / filename
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )

@router.get("/download/script/{filename}")
def download_script(filename: str):
    file_path = ARTIFACT_DIR / filename
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )