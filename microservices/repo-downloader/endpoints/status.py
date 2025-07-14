from fastapi import APIRouter

router = APIRouter(prefix="/v1")

@router.get("/status", summary="Check the status of the API.")
def get_status():
    return {"message": "Ok"}