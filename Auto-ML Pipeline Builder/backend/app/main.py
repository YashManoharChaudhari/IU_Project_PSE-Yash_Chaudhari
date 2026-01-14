from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routes import router

app = FastAPI(title="Auto-ML Pipeline Builder")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# -----------------------------
# Serve artifacts for download
# -----------------------------
ARTIFACT_DIR = Path(__file__).parent.parent / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)

app.mount(
    "/artifacts",
    StaticFiles(directory=ARTIFACT_DIR),
    name="artifacts",
)