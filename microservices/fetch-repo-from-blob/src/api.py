from fastapi import APIRouter
from .service import download_and_validate_blobs

router = APIRouter()

@router.get("/validate-blobs/{container_name}")
def validate_blobs(container_name: str):
    valid_blobs = download_and_validate_blobs(container_name)
    return {"Valid blobs": valid_blobs}

@router.get("/access-blob/{container_name}/{blob_name}")
def is_blob_accessible(container_client, blob_name):
    accessible_blob = is_blob_accessible(container_client, blob_name)
    return {"Blob accessible": accessible_blob}
