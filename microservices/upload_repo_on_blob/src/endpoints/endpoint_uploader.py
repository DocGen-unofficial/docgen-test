from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict
from src.services.blob_manager import BlobManager
from src.services.uploader import RepoUploader

router = APIRouter(prefix="/v2")

@router.get("/repo/check_connection")
async def check_connection():
    """
    Verify the connection to Azure Blob Storage.

    Returns:
        dict: A JSON response indicating whether the connection to Azure Blob Storage
        was successful or failed, including an error message if applicable.
    """
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
    """
    Upload a local repository to Azure Blob Storage.

    Attributes:
        repo_path (str): The local file system path of the repository to be uploaded.

    Returns:
        dict:
          - message (str): Status message about the cloning operation
        - path (str, optional): Path where repository was cloned (if successful)
            - Url (str, optional): Repository URL (if successful) A JSON response indicating the status of the upload operation and
        the name of the container where the repository was uploaded, or an error message if the upload failed.
    """
    try:
        blobmanager = BlobManager()
        uploader = RepoUploader(blobmanager)
        container = uploader.upload_repository(repo_path)
        return {
            "status": "success",
            "container_name": container
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to connect to Azure Blob Storage.",
            "error": str(e)
        }
