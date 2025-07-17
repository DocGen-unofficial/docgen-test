from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import tempfile
import os
import time
from typing import Any

from src.services.blob_manager import BlobManager
from src.services.uploader import RepoUploader
from src.utils.helpers import sanitize_container_name
from src.utils.logging_config import get_logger
from src.utils.log_messages import (
    upload_started,
    upload_success,
    upload_failed,
)

logger = get_logger(__name__)
app = FastAPI()

@app.post("/upload-repo")
async def upload_repo(file: UploadFile = File(...)) -> JSONResponse:
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path: str = os.path.join(tmpdir, file.filename)
        with open(repo_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        container_name: str = sanitize_container_name(os.path.splitext(file.filename)[0])
        logger.info(upload_started(repo_path, container_name))
        start_time: float = time.time()

        try:
            with BlobManager() as blob_manager:
                uploader: RepoUploader = RepoUploader(blob_manager, logger)
                total_files: int = uploader.upload_repository(tmpdir, container_name)

            elapsed_time: float = time.time() - start_time
            logger.info(upload_success(repo_path, total_files, elapsed_time))
            return JSONResponse(status_code=200, content={
                "message": "Upload completed",
                "container": container_name,
                "elapsed_time": round(elapsed_time, 2)
            })
        except Exception as e:
            elapsed_time: float = time.time() - start_time
            logger.error(upload_failed(repo_path, elapsed_time, e))
            raise HTTPException(status_code=500, detail="Upload failed")
