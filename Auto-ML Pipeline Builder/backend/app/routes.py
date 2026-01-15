from fastapi import APIRouter, UploadFile, File
from .models import PipelineCreateRequest
from .services import (
    save_dataset,
    create_pipeline,
    execute_pipeline_async,
    list_pipelines,
    get_pipeline,
    download_pipeline_script,
)

router = APIRouter()

@router.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    return save_dataset(file)

@router.post("/pipeline")
def create_pipeline_route(req: PipelineCreateRequest):
    return create_pipeline(req)

@router.post("/pipeline/{pipeline_id}/execute")
def run_pipeline(pipeline_id: int):
    execute_pipeline_async(pipeline_id)
    return {"status": "started"}

@router.get("/pipelines")
def pipelines():
    return list_pipelines()

@router.get("/pipeline/{pipeline_id}")
def pipeline_details(pipeline_id: int):
    return get_pipeline(pipeline_id)

@router.get("/pipeline/{pipeline_id}/download-script")
def download_script(pipeline_id: int):
    return download_pipeline_script(pipeline_id)