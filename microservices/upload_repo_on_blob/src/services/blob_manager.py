from azure.storage.blob import BlobServiceClient
from src.config.settings import Settings

class BlobManager:
    def __init__(self):
        if not Settings.CONNECTION_STRING:
            raise ValueError("Missing AZURE_STORAGE_CONNECTION_STRING")
        self.client = BlobServiceClient.from_connection_string(Settings.CONNECTION_STRING)

    def ensure_container_exists(self, container_name: str):
        container_client = self.client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
        return container_client

    def __repr__(self):
        return f"{self.__class__.__name__}(connected=True)"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

