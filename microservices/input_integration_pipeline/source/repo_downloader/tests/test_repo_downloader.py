from source.github_cloner import DownloadRepo, InvalidLinkRepository
import pytest, requests

def test_not_valid_url() -> None:
    """
    Test to verify that the application correctly recognizes invalid URLs.
    """
    url_repository = "https://www.google.com/"
    with pytest.raises(InvalidLinkRepository):
        DownloadRepo(url_repository)

def test_valid_url() -> None:
    """
    Test to verify that the application correctly recognizes valid GitHub repository URLs.
    """
    url_repository = "https://github.com/pandas-dev/pandas.git"
    repo = DownloadRepo(url_repository)
    assert isinstance(repo, DownloadRepo)

def test_list_valid_url() -> None:
    """
    Test to verify that the application correctly recognizes a list of valid GitHub repository URLs.
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
    Test to verify that the API connection is established and responding.
    """
    response = requests.get(url='http://127.0.0.1:8081/v1/status')
    assert response.json()["message"] == "Ok"

def test_cloning_public_repository() -> None:
    """
    Test to verify that public repository cloning is successful via the API.
    """
    response = requests.post(
        url='http://127.0.0.1:8081/v1/download_repository', 
        json={
            "repository": "https://github.com/robertoparodo/UnicAssistant.git"
        }
    )
    assert "Repository successfully cloned." == response.json()["message"]

def test_cloning_private_repository() -> None:
    """
    Test to verify that private repository cloning is successful via the API.
    """
    response = requests.post(
        url='http://127.0.0.1:8081/v1/download_repository', 
        json={
            "repository": "https://github.com/chrisputzu/docgentest_private_repo.git",
            "token": "<here you have to enter your personal token>"
        }
    )
    assert "Repository successfully cloned." == response.json()["message"]
