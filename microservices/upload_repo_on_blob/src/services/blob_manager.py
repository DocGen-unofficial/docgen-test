from azure.storage.blob import BlobServiceClient, ContainerClient
from src.config.settings import Settings

class BlobManager:
    def __init__(self):
        self._connect()

    def _connect(self):
        if not Settings.CONNECTION_STRING:
            raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING must be set in the environment.")
        try:
            self.service_client = BlobServiceClient.from_connection_string(Settings.CONNECTION_STRING)
            self.service_client.get_service_properties()  # validazione reale
        except Exception as e:
            raise RuntimeError(f"BlobManager failed to connect to Azure Blob Storage: {e}")
        
    def ensure_container_exists(self, container_name: str) -> ContainerClient:
        container_client: ContainerClient = self.service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
        return container_client
