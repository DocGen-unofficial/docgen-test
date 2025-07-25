import os
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from azure.storage.blob import ContainerClient
from pydantic import BaseModel, Field
from src.services.blob_manager import BlobManager
from src.utils.helpers import sanitize_container_name, is_path_allowed


class RepoUploader:
    """
    Uploads a local repository to Azure Blob Storage.
    """

    def __init__(self, blob_manager: BlobManager):
        """
        Args:
            blob_manager (BlobManager): Blob manager used to access Azure Storage.
        """
        self.blob_manager = blob_manager

    def upload_repository(self, repo_path: str, max_workers: int = 8) -> Tuple[str, bool]:
        """
        Uploads files from a local repo to Azure, syncing the container.

        Args:
            repo_path (str): Path to the local repository.
            max_workers (int): Number of threads for parallel upload.

        Returns:
            Tuple[str, bool]: Container name and True if created, else False.
        """
        container_name = sanitize_container_name(os.path.basename(os.path.normpath(repo_path)))
        container_client, created = self.blob_manager.ensure_container_exists(container_name)
        files: List[Tuple[str, str]] = []
        for root, _, filenames in os.walk(repo_path):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, repo_path).replace("\\", "/")
                if not is_path_allowed(relative_path):
                    continue
                files.append((full_path, relative_path))
        existing_blobs = self.blob_manager.get_blob_name_set(container_name)
        local_paths = {rel for _, rel in files}
        to_delete = existing_blobs - local_paths
        for blob_name in to_delete:
            container_client.delete_blob(blob_name)
        self._speed_up_upload(container_client, files, max_workers)
        return container_name, created

    def _speed_up_upload(self, container_client: ContainerClient, files: List[Tuple[str, str]], max_workers: int):
        """
        Uploads files in parallel using threads.

        Args:
            container_client (ContainerClient): Target container.
            files (List[Tuple[str, str]]): List of (full_path, relative_path).
            max_workers (int): Number of threads.
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.upload_single_file, container_client, full, rel)
                for full, rel in files
            ]
            for future in as_completed(futures):
                future.result()

    def upload_single_file(self, container_client: ContainerClient, full_path: str, relative_path: str):
        """
        Uploads a single file to Azure Blob Storage.

        Args:
            container_client (ContainerClient): Target container.
            full_path (str): Absolute path to the file.
            relative_path (str): Relative path used as blob name.
        """
        blob_client = container_client.get_blob_client(relative_path)
        with open(full_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

