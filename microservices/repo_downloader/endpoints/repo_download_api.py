from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict
from source.github_cloner import DownloadRepo

router = APIRouter(prefix="/v1")

class GithubRepository(BaseModel):
    repository: str = Field(
        ...,
        example="",
        description="Full name of the GitHub repository (e.g., 'owner/repo')"
    )
    token: Optional[str] = Field(
        default=None,
        example="",
        description="Optional GitHub access token (can be omitted or set to null)"
    )

@router.post("/download_repository", summary="Endpoint to clone a repository")
async def download_repository(repository: GithubRepository) -> Dict:
    
    try:
        repo = DownloadRepo(repository.repository, repository.token)
    except:
        return{'message': 'Link to repository invalid or not found'}
    
    repo = repo.download()
    if repo[0]:
        return {"message": f"Repository successfully cloned. Local path: {repo[1]}. Url repository: {repo[2]}"}
    return {"message": "cloning error"}