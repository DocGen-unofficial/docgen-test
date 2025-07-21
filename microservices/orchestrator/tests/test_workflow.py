import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import requests

import main
from source import apicalls

from typing import Any, Optional
from types import SimpleNamespace

MOCK_ENDPOINT = "http://localhost:5999/mock"

def mock_get(url: str):
    return SimpleNamespace(status_code=200)

def mock_post_success(url: str, json: dict):
    return SimpleNamespace(status_code=200, json=lambda: {"path": "/mock/path"})

def mock_post_failure(url: str, json: dict):
    return SimpleNamespace(status_code=404, text="Not found", json=lambda: {})

def mock_post_workflow(url: str, json: Optional[dict] = None, params: Optional[dict] = None):
    if "download_repository" in url:
        resp = SimpleNamespace(status_code=200, json=lambda: {"path": "/mock/path"})
    elif "repo/upload" in url:
        resp = SimpleNamespace(status_code=200, json=lambda: {"container_name": "mock_container"})
    elif "transform-container-to-parquet" in url:
        resp = SimpleNamespace(status_code=200, json=lambda: {"message": "Transformation complete"})
    else:
        resp = SimpleNamespace(status_code=200, json=lambda: {})
    mock_post_workflow.calls.append(url)
    return resp

def test_get_repo_status(monkeypatch: Any) -> None:
    """
    Test get_repo_status to ensure it returns the correct status code.
    Attributes:
        monkeypatch (Any): Pytest fixture for patching functions.
    Returns:
        None
    """
    monkeypatch.setattr(requests, "get", mock_get)
    status = apicalls.get_repo_status(MOCK_ENDPOINT)
    assert status == 200

def test_get_repo_url_success(monkeypatch: Any) -> None:
    """
    Test get_repo_url for a successful response.
    Attributes:
        monkeypatch (Any): Pytest fixture for patching functions.
    Returns:
        None
    """
    monkeypatch.setattr(requests, "post", mock_post_success)
    result = apicalls.get_repo_url(MOCK_ENDPOINT, {"repository": "repo"})
    assert result == "/mock/path"

def test_get_repo_url_failure(monkeypatch: Any) -> None:
    """
    Test get_repo_url for a failed response (status code != 200).
    Attributes:
        monkeypatch (Any): Pytest fixture for patching functions.
    Returns:
        None
    """
    monkeypatch.setattr(requests, "post", mock_post_failure)
    result = apicalls.get_repo_url(MOCK_ENDPOINT, {"repository": "repo"})
    assert result is None

def test_main_workflow(monkeypatch: Any) -> None:
    """
    Test the main workflow by mocking requests.post to simulate downstream services.
    Attributes:
        monkeypatch (Any): Pytest fixture for patching functions.
    Returns:
        None
    """
    mock_post_workflow.calls = []
    monkeypatch.setattr(requests, "post", mock_post_workflow)
    main.__name__ = "__main__"
    try:
        exec(open("main.py").read(), main.__dict__)
    except Exception as e:
        pytest.fail(f"Workflow failed: {e}")
    assert len(mock_post_workflow.calls) == 3

if __name__ == "__main__":
    sys.exit(pytest.main([__file__])) 