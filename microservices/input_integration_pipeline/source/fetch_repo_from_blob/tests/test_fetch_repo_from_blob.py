import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from source.blob_services import get_blob_from_container, blob_to_parquet
from source.container_services import access_container, get_container, get_files_by_type, container_to_parquet


@pytest_asyncio.fixture
def mock_blob_client():
    mock = AsyncMock()
    mock.download_blob.return_value.readall.return_value = b"test content"
    return mock

@pytest_asyncio.fixture
def mock_container_client_fixture():
    from unittest.mock import MagicMock, AsyncMock

    mock = MagicMock()
    mock.get_container_properties = AsyncMock(return_value={})

    class AsyncBlobIterator:
        def __aiter__(self):
            async def gen():
                blob_mock = MagicMock()
                blob_mock.name = "test_blob.txt"
                yield blob_mock
            return gen()

    def list_blobs(*args, **kwargs):
        return AsyncBlobIterator()
    mock.list_blobs = list_blobs

    def get_blob_client(name):
        blob_client_mock = AsyncMock()
        blob_client_mock.download_blob.return_value.readall.return_value = b"test content"
        blob_client_mock.download_blob.return_value = AsyncMock()
        blob_client_mock.download_blob.return_value.readall.return_value = b"test content"
        return blob_client_mock
    mock.get_blob_client.side_effect = get_blob_client

    return mock

@pytest.fixture(autouse=True)
def patch_blob_service_client(monkeypatch, mock_container_client_fixture):
    from source import container_services, blob_services
    monkeypatch.setattr(container_services, "blob_service_client", MagicMock(get_container_client=MagicMock(return_value=mock_container_client_fixture)))
    monkeypatch.setattr(blob_services, "blob_service_client", MagicMock(get_container_client=MagicMock(return_value=mock_container_client_fixture)))

@pytest.mark.asyncio
@patch('source.blob_services.blob_service_client')
async def test_get_blob_from_container(mock_blob_service_client, mock_blob_client):
    mock_blob_service_client.get_container_client.return_value.get_blob_client.return_value = mock_blob_client
    result = await get_blob_from_container('testcontainer', 'testblob.txt')
    assert result["status"] is True
    assert "downloaded successfully" in result["details"]

@pytest.mark.asyncio
@patch('source.blob_services.blob_service_client')
async def test_blob_to_parquet(mock_blob_service_client, mock_blob_client):
    mock_blob_service_client.get_container_client.return_value.get_blob_client.return_value = mock_blob_client
    result = await blob_to_parquet('testcontainer', 'testblob.txt')
    assert result["status"] is True
    assert result["parquet_path"].endswith('.parquet')

@pytest.mark.asyncio
@patch("source.container_services.blob_service_client")
async def test_access_container(mock_blob_service_client, mock_container_client_fixture):
    mock_blob_service_client.get_container_client.return_value = mock_container_client_fixture
    result = await access_container("test-container")
    assert result["status"] is True

@pytest.mark.asyncio
@patch("source.container_services.blob_service_client")
async def test_get_container(mock_blob_service_client, mock_container_client_fixture):
    mock_blob_service_client.get_container_client.return_value = mock_container_client_fixture
    result = await get_container("test-container")
    assert result["status"] is True
    assert "Downloaded" in result["details"]

@pytest.mark.asyncio
@patch("source.container_services.blob_service_client")
async def test_get_files_by_type(mock_blob_service_client, mock_container_client_fixture):
    mock_blob_service_client.get_container_client.return_value = mock_container_client_fixture
    result = await get_files_by_type("test-container", ".txt")
    assert result["status"] is True

@pytest.mark.asyncio
@patch("source.container_services.blob_service_client")
async def test_container_to_parquet(mock_blob_service_client, mock_container_client_fixture):
    mock_blob_service_client.get_container_client.return_value = mock_container_client_fixture
    result = await container_to_parquet("test-container", single_parquet=True)
    assert result["status"] is True
    assert result["parquet_path"].endswith(".parquet")

