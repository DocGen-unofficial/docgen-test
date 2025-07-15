from source.github_cloner import DownloadRepo, InvalidLinkRepository
import pytest, requests

def test_not_valid_url() -> None:
    """
    Test to verify that with a wrong URL the application recognizes it
    """
    url_repository = "https://www.google.com/"
    with pytest.raises(InvalidLinkRepository):
        DownloadRepo(url_repository)

def test_valid_url() -> None:
    """
    Test to see if it recognizes repository links
    """
    url_repository = "https://github.com/pandas-dev/pandas.git"
    repo = DownloadRepo(url_repository)
    assert isinstance(repo, DownloadRepo)

def test_list_valid_url() -> None:
    """
    Test to see if the list of GitHub URLs is correct
    """
    repository_list = [
        "https://github.com/theskumar/python-dotenv.git",
        "https://github.com/scrapy/scrapy.git",
        "https://github.com/pallets/flask.git",
        "https://github.com/fastapi/fastapi.git",
        "https://github.com/pytorch/pytorch.git",
        "https://github.com/django/django.git",
        "https://github.com/numpy/numpy.git",
        "https://github.com/matplotlib/matplotlib.git",
        "https://github.com/scikit-learn/scikit-learn.git",
        "https://github.com/python-pillow/Pillow.git",
        "https://github.com/sqlalchemy/sqlalchemy.git",
        "https://github.com/sympy/sympy.git",
    ]
    for url in repository_list:
        repo = DownloadRepo(url)
        assert isinstance(repo, DownloadRepo)

def test_connection() -> None:
    """
    Test to see if the connection is established
    """
    response = requests.get(url='http://127.0.0.1:8081/v1/status')
    assert response.json()["message"] == "Ok"

def test_cloning_pubblic_repository() -> None:
    """
    Test to see if pubblic repository cloning is successful
    """
    response = requests.post(
        url='http://127.0.0.1:8081/v1/download_repository', 
        json={
            "repository": "https://github.com/robertoparodo/UnicAssistant.git"
        }
    )
    assert response.json()["message"] == "successful cloning"

def test_cloning_private_repository() -> None:
    """
    Test to see if private repository cloning is successful
    """
    response = requests.post(
        url='http://127.0.0.1:8081/v1/download_repository', 
        json={
            "repository": "https://github.com/chrisputzu/docgentest_private_repo.git",
            "token": "<here you have to enter your personal token>"
        }
    )
    assert response.json()["message"] == "successful cloning"
