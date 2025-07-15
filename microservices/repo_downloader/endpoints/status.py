from fastapi import APIRouter
from typing import Dict

router = APIRouter(prefix="/v1")

@router.get("/status", summary="Check the status of the API.")
def get_status() -> Dict:
    return {"message": "Ok"}