from source.github_cloner import DownloadRepo, InvalidLinkRepository
import pytest, requests

def test_not_valid_url():
    """
    Test to verify that with a wrong URL the application recognizes it
    """
    url_repository = "https://www.google.com/"
    with pytest.raises(InvalidLinkRepository):
        DownloadRepo(url_repository)

def test_valid_url():
    """
    Test to see if it recognizes repository links
    """
    url_repository = "https://github.com/pandas-dev/pandas.git"
    repo = DownloadRepo(url_repository)
    assert isinstance(repo, DownloadRepo)

def test_connection():
    """
    Test to see if the connection is established
    """
    response = requests.get(url='http://127.0.0.1:8081/v1/status')
    assert response.json()["message"] == "Ok"

def test_cloning_api():
    """
    Test to see if repository cloning is successful
    """
    response = requests.post(
        url='http://127.0.0.1:8081/v1/download_repository', 
        json={
            "repository": "https://github.com/robertoparodo/UnicAssistant.git"
        }
    )
    assert response.json()["message"] == "successful cloning"
