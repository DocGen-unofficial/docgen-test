from typing import Optional
import os, re

LINK = r"^https?:\/\/(www\.)?github\.com\/[\w.-]+\/[\w.-]+\.git$"

class DownloadRepo():
    """
    This class is used to clone a repository from github

    Attributes:
        url_repository (str): Repository URL link 
        token (str): Your token to clone your private repository
    """
    def __init__(self, url_repository: str, token: str = None):
        self.url_repository = url_repository
        self.token = token
        self.github_folder_name = self.url_repository.split("/")[-1].replace(".git","")
        self.__check_url()
        self.__add_token()
        

    def __check_url(self) -> None:
        """
        Method to check if the link is a github repository
        """
        if not re.match(LINK, self.url_repository):
            raise InvalidLinkRepository(self.url_repository)
        
    def __add_token(self) -> None:
        """
        Method that adds the token to download a private repository 
        """
        if self.token:
            self.url_repository = re.sub(r'^(https?://)', rf'\1{self.token}@', self.url_repository)

    def __is_git_cloned(self) -> str:
        """
        Method to create the path where the repository will be stored

        Returns:
            str: The directory path
        """
        full_path = os.path.join(os.getcwd(), "outputs", self.github_folder_name)
        return full_path

    def download(self) -> tuple[bool, str, str]:
        """
        Clone a repository

        Returns:
            tuple[bool, str]: A tuple where:
                - The first element is True if the repository was cloned successfully, False otherwise
                - The second element is the path where the repository is (or would be) stored
        """

        os.system(f"git clone {self.url_repository} outputs/{self.github_folder_name}")
        repo_path = self.__is_git_cloned()
        if os.path.exists(repo_path):
            if self.token:
                self.url_repository = self.url_repository.replace(self.token+"@", "")
            return (True, repo_path, self.url_repository)
        return (False, None, None)
            
            
class InvalidLinkRepository(Exception):
    def __init__(self, link: str):
        super().__init__(f"invalid link to a github repository {link}.")