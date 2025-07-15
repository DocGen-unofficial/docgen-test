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
            self.url_repository = self.url_repository[:8] + self.token +"@"+ self.url_repository[8:]
            print(self.url_repository)

    def download(self) -> bool:
        """
        Clone a repository

        Returns:
            bool: True if the download is successful
        """

        # git clone https://<TOKEN>@github.com/nomeutente/repo-privata.git

        try:
            os.system(f"git clone {self.url_repository}")
            return True
        except:
            return False
            

class InvalidLinkRepository(Exception):
    def __init__(self, link):
        super().__init__(f"invalid link to a github repository {link}.")