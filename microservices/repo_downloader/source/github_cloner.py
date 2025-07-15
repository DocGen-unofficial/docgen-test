from typing import Optional
import os, re

LINK = r"^https?:\/\/(www\.)?github\.com\/[\w.-]+\/[\w.-]+\.git$"

class DownloadRepo():
    """
    This class is used to clone a repository from github

    Attributes:
        url_repository (str): Repository URL link 
        authentication (dict): Login information of a user email, passoword and token
    """
    def __init__(self, url_repository: str, authentication: Optional[dict] = None):
        self.url_repository = url_repository
        self.authentication = authentication
        self.__check_url()

    def __check_url(self):
        """
        Method to check if the link is a github repository
        """
        if not re.match(LINK, self.url_repository):
            raise InvalidLinkRepository(self.url_repository)
    
    def download(self) -> bool:
        """
        Clone a repository

        Returns:
            bool: True if the download is successful
        """
        try:
            os.system(f"git clone {self.url_repository}")
            return True
        except:
            return False


class InvalidLinkRepository(Exception):
    def __init__(self, link):
        super().__init__(f"invalid link to a github repository {link}.")