from typing import Optional, Tuple
import os, re

LINK = r"^https?:\/\/(www\.)?github\.com\/[\w.-]+\/[\w.-]+\.git$"

class DownloadRepo():
    """
    A class to clone repositories from GitHub.

    Attributes:
        url_repository (str): Repository URL link 
        token (Optional[str]): Token to clone private repositories
        github_folder_name (str): Name of the repository folder
    """
    def __init__(self, url_repository: str, token: Optional[str] = None):
        """
        Initialize the DownloadRepo instance.

        Attributes:
            url_repository (str): Repository URL link 
            token (Optional[str]): Token to clone private repositories
        """
        self.url_repository = url_repository
        self.token = token
        self.github_folder_name = self.url_repository.split("/")[-1].replace(".git","")
        self.__check_url()
        self.__add_token()
        

    def __check_url(self) -> None:
        """
        Check if the URL is a valid GitHub repository link.
        
        Raises:
            InvalidLinkRepository: If the URL is not a valid GitHub repository link
        """
        if not re.match(LINK, self.url_repository):
            raise InvalidLinkRepository(self.url_repository)
        
    def __add_token(self) -> None:
        """
        Add authentication token to the repository URL for private repositories.
        """
        if self.token:
            self.url_repository = re.sub(r'^(https?://)', rf'\1{self.token}@', self.url_repository)

    def __is_git_cloned(self) -> str:
        """
        Get the path where the repository will be stored.

        Returns:
            str: The directory path where the repository is stored
        """
        full_path = os.path.join(os.getcwd(), "outputs", self.github_folder_name)
        return full_path

    def download(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Clone a repository to the local system.

        Returns:
            Tuple[bool, Optional[str], Optional[str]]: A tuple containing:
                - bool: True if repository was cloned successfully, False otherwise
                - Optional[str]: Path where repository is stored (None if failed)
                - Optional[str]: Repository URL (None if failed)
        """

        os.system(f"git clone {self.url_repository} outputs/{self.github_folder_name}")
        repo_path = self.__is_git_cloned()
        if os.path.exists(repo_path):
            if self.token:
                self.url_repository = self.url_repository.replace(self.token+"@", "")
            return (True, repo_path, self.url_repository)
        return (False, None, None)
            
            
class InvalidLinkRepository(Exception):
    """
    Exception raised when the provided link is not a valid GitHub repository.
    """
    def __init__(self, link: str):
        """
        Initialize the exception with the invalid link.

        Attributes:
            link (str): The invalid repository link
        """
        super().__init__(f"Invalid link to a GitHub repository: {link}")