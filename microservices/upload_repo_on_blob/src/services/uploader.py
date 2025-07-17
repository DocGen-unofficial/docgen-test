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

import os
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from azure.storage.blob import ContainerClient

from src.services.blob_manager import BlobManager
from src.utils.helpers import sanitize_container_name

class RepoUploader:
    def __init__(self, blob_manager: BlobManager):
        self.blob_manager = blob_manager


    def upload_single_file(self, container_client: ContainerClient, full_path: str, relative_path: str) -> None:
       
        blob_client = container_client.get_blob_client(relative_path)
        with open(full_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

    def _speed_up_upload(self,container_client: ContainerClient,files: List[Tuple[str, str]],max_workers: int):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.upload_single_file, container_client, full, rel)
                for full, rel in files
            ]
            for future in as_completed(futures):
                future.result()
    
    def upload_repository(self, repo_path: str, max_workers: int = 8) -> int:
        container_name = sanitize_container_name(os.path.basename(os.path.normpath(repo_path)))
        container_client = self.blob_manager.ensure_container_exists(container_name)
        files: List[Tuple[str, str]] = []
        for root, _, filenames in os.walk(repo_path):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, repo_path).replace("\\", "/")
                files.append((full_path, relative_path))
        self._speed_up_upload(container_client, files, max_workers)
        return len(files)

