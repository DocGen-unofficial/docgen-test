from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict
from source.github_cloner import DownloadRepo

router = APIRouter(prefix="/v1", tags = ["Clone repository"])

class GithubRepository(BaseModel):
    """
    Pydantic model for validating GitHub repository download requests.

    Attributes:
        repository (str): Full name of the GitHub repository (e.g., 'owner/repo')
        token (Optional[str]): Optional GitHub access token for private repositories
    """
    repository: str = Field(
        ...,
        description="Full name of the GitHub repository (e.g., 'owner/repo')"
    )
    token: Optional[str] = Field(
        default=None,
        description="Optional GitHub access token for private repositories"
    )

@router.post("/download_repository", summary="Endpoint to clone a repository")
async def download_repository(repository: GithubRepository) -> Dict:
    """
    Download and clone a repository from GitHub.

    Attributes:
        repository (GithubRepository): The repository data containing URL and optional token

    Returns:
        Dict: A dictionary containing:
            - message (str): Status message about the cloning operation
            - path (str, optional): Path where repository was cloned (if successful)
            - Url (str, optional): Repository URL (if successful)
    """
    try:
        repo = DownloadRepo(repository.repository, repository.token)
    except:
        return{'message': 'Link to repository invalid or not found'}
    
    repo = repo.download()
    if repo[0]:
        return {"message": "Repository successfully cloned.",  "path": repo[1],  "Url":repo[2]}
    return {"message": "cloning error"}