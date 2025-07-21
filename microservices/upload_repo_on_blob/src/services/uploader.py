import os
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from azure.storage.blob import ContainerClient
from src.utils.helpers import sanitize_container_name
# sviluppo futuro: creare un conteiner per cliente/business unit che ospiterà piu repository gestione con urlparse
# esempio url github:
# id.utente (uuid) 
#   github.com 
#       nome_utente
#           nome_repository
#dubbio le repo sono pronte? oppure si deve tenere conto di repository che potrebbero essere aggiornate nel tempo?
import os
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from azure.storage.blob import ContainerClient

from src.services.blob_manager import BlobManager
from src.utils.helpers import sanitize_container_name

class RepoUploader:
    """
    Handles the upload of a local repository to Azure Blob Storage.

    This class is responsible for:
    - Ensuring the container exists (creating it if necessary).
    - Scanning the local repository recursively.
    - Uploading all files to Azure Blob Storage using parallel threads.
    """

    def __init__(self, blob_manager: BlobManager):
        """
        Initialize the RepoUploader.

        Args:
            blob_manager (BlobManager): Instance responsible for managing Azure container operations.
        """
        self.blob_manager = blob_manager

    def upload_repository(self, repo_path: str, max_workers: int = 8) -> Tuple[str, bool]:
        """
        Upload all files from a local repository to an Azure Blob Storage container.

        The container name is derived from the repository path and sanitized to meet
        Azure naming rules. If the container does not exist, it is created.
        Files are uploaded concurrently.

        Args:
            repo_path (str): Path to the local repository directory.
            max_workers (int, optional): Maximum number of threads for parallel upload. Defaults to 8.

        Returns:
            Tuple[str, bool]: A tuple containing:
                - str: Name of the container.
                - bool: True if the container was created, False if it already existed.
        """
        container_name = sanitize_container_name(os.path.basename(os.path.normpath(repo_path)))
        container_client, created = self.blob_manager.ensure_container_exists(container_name)

        files: List[Tuple[str, str]] = []
        for root, _, filenames in os.walk(repo_path):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, repo_path).replace("\\", "/")
                files.append((full_path, relative_path))

        self._speed_up_upload(container_client, files, max_workers)
        return container_name, created

    def _speed_up_upload(self, container_client: ContainerClient, files: List[Tuple[str, str]], max_workers: int):
        """
        Upload multiple files in parallel to Azure Blob Storage using a thread pool.

        Args:
            container_client (ContainerClient): The Azure container client.
            files (List[Tuple[str, str]]): List of (full_path, relative_path) file tuples.
            max_workers (int): Number of threads to use for concurrent uploads.
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.upload_single_file, container_client, full, rel)
                for full, rel in files
            ]
            for future in as_completed(futures):
                future.result()

    def upload_single_file(self, container_client: ContainerClient, full_path: str, relative_path: str) -> None:
        """
        Upload a single file to Azure Blob Storage.

        If a blob with the same name already exists, it will be overwritten
        unless handled differently.

        Args:
            container_client (ContainerClient): The Azure container client.
            full_path (str): Absolute path to the file on the local filesystem.
            relative_path (str): Path used as the blob name in the container.
        """
        blob_client = container_client.get_blob_client(relative_path)
        with open(full_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)  # consider overwrite=False for production
