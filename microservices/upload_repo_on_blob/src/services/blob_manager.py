from typing import Tuple
from azure.storage.blob import BlobServiceClient, ContainerClient
from src.config.settings import Settings

from typing import Tuple
from azure.storage.blob import BlobServiceClient, ContainerClient
from src.config.settings import Settings

class BlobManager:
    """
    Manages the connection and interaction with Azure Blob Storage.

    This class handles:
    - Initialization of the BlobServiceClient using a connection string.
    - Validation of the connection.
    - Creation or retrieval of containers.
    """

    def __init__(self):
        """
        Initialize a BlobManager instance and connect to Azure Blob Storage.
        """
        self._connect()

    def _connect(self):
        """
        Establish a connection to Azure Blob Storage using the connection string
        defined in the environment variable `AZURE_STORAGE_CONNECTION_STRING`.

        Raises:
            RuntimeError: If the connection string is missing or the connection fails.
        """
        if not Settings.CONNECTION_STRING:
            raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING must be set in the environment.")
        try:
            self.service_client = BlobServiceClient.from_connection_string(Settings.CONNECTION_STRING)
            self.service_client.get_service_properties()  # Trigger actual connection validation
        except Exception as e:
            raise RuntimeError(f"BlobManager failed to connect to Azure Blob Storage: {e}")

    def ensure_container_exists(self, container_name: str) -> Tuple[ContainerClient, bool]:
        """
        Ensure that a container exists in Azure Blob Storage.

        If the specified container does not exist, it will be created.

        Args:
            container_name (str): The name of the container to check or create.

        Returns:
            Tuple[ContainerClient, bool]: A tuple where:
                - The first element is the ContainerClient for the specified container.
                - The second element is True if the container was created, False if it already existed.
        """
        container_client: ContainerClient = self.service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
            return container_client, True
        return container_client, False
