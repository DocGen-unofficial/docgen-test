from typing import Optional, Tuple
import shutil
import os, re

LINK = r"^https?:\/\/(www\.)?github\.com\/[\w.-]+\/[\w.-]+\.git$"

class DownloadRepo():
    """
    A class to clone repositories from GitHub.

    Attributes:
        url_repository (str): Repository URL link 
        token (Optional[str]): Token to clone private repositories
    """
    def __init__(self, url_repository: str, token: Optional[str] = None):
        self.url_repository = url_repository
        self.token = token
        self.__check_url()
        self.__create_unique_name()
        self.__add_token()
        

    def __check_url(self) -> None:
        """
        Check if the URL is a valid GitHub repository link.
        
        Raises:
            InvalidLinkRepository: If the URL is not a valid GitHub repository link
        """
        if not re.match(LINK, self.url_repository):
            raise (f"Invalid link to a GitHub repository: {self.url_repository}")
        
    def __create_unique_name(self) -> None:
        """
        Method to create unique repository name 
        """
        temp_folder_name = self.url_repository.lower().replace(".git","").split("/")[-2:]
        self.github_folder_name = "-".join(temp_folder_name)
        
    def __add_token(self) -> None:
        """
        Add authentication token to the repository URL for private repositories.
        """
        if self.token:
            self.url_repository = re.sub(r'^(https?://)', rf'\1{self.token}@', self.url_repository)

    def __get_repository_path(self) -> str:
        """
        Get the path where the repository will be stored.

        Returns:
            str: The directory path where the repository is stored
        """
        full_path = os.path.join(os.getcwd(), "outputs", self.github_folder_name)
        return full_path

    def download(self) -> str:
        """
        Clone a repository to the local system.

        Returns:
            str: Path where repository is stored (None if failed)
        """
        repo_path = self.__get_repository_path()
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
        os.system(f"git clone {self.url_repository} outputs/{self.github_folder_name}")
        if self.token:
            self.url_repository = self.url_repository.replace(self.token+"@", "")
        if os.path.exists(repo_path) and any(os.scandir(repo_path)):
            return repo_path
        raise("Cloning failed")
