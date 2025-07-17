from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict
from src.services.blob_manager import BlobManager
from src.services.uploader import RepoUploader

router = APIRouter(prefix="/v2")

@router.get("/repo/check_connection")
async def check_connection():
    """
    Check if the connection to Azure Blob Storage is successful.
    """
    try:
        blobmanager = BlobManager()
        return {"status": "success", "message": "Connection to Azure Blob Storage is successful."}
    except Exception as e:
        return {"status": "error", "message": "Failed to connect to Azure Blob Storage.", "error": str(e)}
    

@router.post("/repo/upload")
async def upload_repo(repo_path: str)-> Dict[str, str]: 
    blobmanager = BlobManager()
    uploader = RepoUploader(blobmanager, logger=None)
    upload_file = uploader.upload_repository(repo_path)
    return {"status": "success", "message": f"Uploaded {upload_file}"}



