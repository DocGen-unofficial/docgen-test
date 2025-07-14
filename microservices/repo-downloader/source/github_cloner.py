import os, re

LINK = r"^https?:\/\/(www\.)?github\.com\/[\w.-]+\/[\w.-]+\.git$"

class DownloadRepo():
    def __init__(self, url_repository: str, 
                 authentication: dict = {'email': None, 'password': None}):
        self.url_repository = url_repository
        self.authentication = authentication
        self.__check_url()

    def __check_url(self):
        if not re.match(LINK, self.url_repository):
            raise InvalidLinkRepository(self.url_repository)
    
    def download(self) -> bool:
        try:
            os.system(f"git clone {self.url_repository}")
            return True
        except:
            print("Downloaded Failed")
            return False


class InvalidLinkRepository(Exception):
    def __init__(self, link):
        super().__init__(f"invalid link to a github repository {link}.")