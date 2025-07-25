import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app


client = TestClient(app)

@patch("src.endpoints.endpoint_uploader.BlobManager")
def test_check_connection_success(mock_blob_manager):
    """
    Verifica che la connessione vada a buon fine.
    """
    response = client.get("/v2/repo/check_connection")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert "Connection to Azure Blob Storage is successful" in body["message"]

@patch("src.endpoints.endpoint_uploader.BlobManager", side_effect=Exception("Connection failed"))
def test_check_connection_failure(mock_blob_manager):
    """
    Verifica il comportamento in caso di errore durante la connessione.
    """
    response = client.get("/v2/repo/check_connection")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "error"
    assert body["message"] == "Failed to connect to Azure Blob Storage."
    assert "Connection failed" in body["error"]

@patch("src.endpoints.endpoint_uploader.RepoUploader")
@patch("src.endpoints.endpoint_uploader.BlobManager")
def test_upload_repo_success(mock_blob_manager, mock_repo_uploader):
    """
    Verifica che l'upload della repository vada a buon fine.
    """
    mock_instance = mock_repo_uploader.return_value
    mock_instance.upload_repository.return_value = ("mock-container", True)

    response = client.post("/v2/repo/upload", params={"repo_path": "/mock/path"})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["container_name"] == "mock-container"
    assert "created" in body["message"]

@patch("src.endpoints.endpoint_uploader.RepoUploader", side_effect=Exception("Upload failed"))
@patch("src.endpoints.endpoint_uploader.BlobManager")
def test_upload_repo_failure(mock_blob_manager, mock_repo_uploader):
    """
    Verifica il comportamento in caso di errore durante l'upload.
    """
    response = client.post("/v2/repo/upload", params={"repo_path": "/mock/path"})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "error"
    assert "Upload failed" in body["error"]