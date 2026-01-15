from pydantic import BaseModel

class PipelineCreateRequest(BaseModel):
    dataset_path: str
    target_column: str