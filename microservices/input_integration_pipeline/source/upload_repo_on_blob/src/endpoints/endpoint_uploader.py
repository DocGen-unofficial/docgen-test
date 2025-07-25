from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict
from src.services.blob_manager import BlobManager
from src.services.uploader import RepoUploader

router = APIRouter(prefix="/v2")

@router.get("/repo/check_connection")
async def check_connection():
    try:
        blobmanager = BlobManager()
        return {
            "status": "success",
            "message": "Connection to Azure Blob Storage is successful."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to connect to Azure Blob Storage.",
            "error": str(e)
        }

@router.post("/repo/upload")
async def upload_repo(repo_path: str) -> Dict[str, str]:
    try:
        blobmanager = BlobManager()
        uploader = RepoUploader(blobmanager)
        container_name, created = uploader.upload_repository(repo_path)
        return {
            "status": "success",
            "container_name": container_name,
            "message": (
                "Container created." if created 
                    else "Container already existed. Repo synchronized: obsolete blobs removed, current files updated."
            )
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to upload repository to Azure Blob Storage.",
            "error": str(e)
        }


