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

class RepoUploader:
    def __init__(self, blob_manager, logger):
        self.blob_manager = blob_manager
        self.logger = logger

    def upload_file(self, container_client: ContainerClient, full_path: str, relative_path: str) -> str:
        blob_client = container_client.get_blob_client(relative_path)
        with open(full_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        return relative_path

    def upload_repository(self, repo_path: str, max_workers: int = 8) -> int:
        container_name = repo_path.split("\\")[-1] # urlparse
        cleaned_container_name = sanitize_container_name(container_name)
        container_client: ContainerClient = self.blob_manager.ensure_container_exists(cleaned_container_name)
        file_paths: List[tuple[str, str]] = []


        for root, _, files in os.walk(repo_path):
            for file in files:
                full_path: str = os.path.join(root, file)
                relative_path: str = os.path.relpath(full_path, repo_path).replace("\\", "/")
                file_paths.append((full_path, relative_path))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.upload_file, container_client, full, rel) for full, rel in file_paths]
            for i, future in enumerate(as_completed(futures), 1):
                _ = future.result()
                if i % 100 == 0:
                    self.logger.info(f"Uploaded {i} files so far...")

        return len(file_paths)
