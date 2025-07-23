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

    Args:
        repo_path (str): The local file system path of the repository to be uploaded.

    Returns:
        Dict[str, str]: A dictionary containing:
            - status: 'success' or 'error'
            - container_name: The name of the container
            - message: Indicates whether the container was created or already existed
    """
    try:
        blobmanager = BlobManager()
        uploader = RepoUploader(blobmanager)
        container_name, created = uploader.upload_repository(repo_path)
        return {
            "status": "success",
            "container_name": container_name,
            "message": "Container created and files uploaded." if created
                       else "Container already existed. Files overwritten."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to connect to Azure Blob Storage.",
            "error": str(e)
        }

