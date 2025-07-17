from azure.storage.blob import BlobServiceClient, ContainerClient
from src.config.settings import Settings

class BlobManager:
    def __init__(self) -> None:
        if not Settings.CONNECTION_STRING:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING must be set in the environment.")
        try:
            self.service_client = BlobServiceClient.from_connection_string(Settings.CONNECTION_STRING)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Azure Blob Storage: {e}")
        

    def __enter__(self) -> "BlobManager":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass  # No explicit cleanup needed

    def ensure_container_exists(self, container_name: str) -> ContainerClient:
        container_client: ContainerClient = self.service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
        return container_client
