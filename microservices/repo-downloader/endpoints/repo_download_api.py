from fastapi import APIRouter
from pydantic import BaseModel
from source.github_cloner import DownloadRepo

class Url(BaseModel):
    repository: str

router = APIRouter(prefix="/v1/download")

@router.post("/download_repository/")
async def download_repository(url_repository: Url):
    repo = DownloadRepo(url_repository.repository)
    if repo.download():
        return {"message": "successful cloning"}
    return {"message": "cloning error"}

