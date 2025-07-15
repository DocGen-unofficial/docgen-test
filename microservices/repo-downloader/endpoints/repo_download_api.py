from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from source.github_cloner import DownloadRepo

router = APIRouter(prefix="/v1")

class Authentication(BaseModel):
    email: Optional[str] = Field(default=None, example=None)
    password: Optional[str] = Field(default=None, example=None)
    token: Optional[str] = Field(default=None, example=None)

class GithubRepository(BaseModel):
    repository: str
    authentication: Optional[Authentication] = Field(
        default=None,
        example={
            "email": None,
            "password": None,
            "token": None
        },
        description="Optional authentication credentials (can be omitted or set to null)"
    )


@router.post("/download_repository", summary="Endpoint to clone a repository")
async def download_repository(repository: GithubRepository):
    
    try:
        repo = DownloadRepo(repository.repository)
    except:
        return{'message': 'Link to repository invalid or not found'}
    
    if repo.download(): #TODO: stampa il percorso dove viene salvata la repo
        return {"message": "successful cloning"}
    return {"message": "cloning error"}