# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.responses import JSONResponse
# import shutil
# import tempfile
# import os
# import time
# from typing import Any

# from src.services.blob_manager import BlobManager
# from src.services.uploader import RepoUploader
# from src.utils.helpers import sanitize_container_name
# from src.utils.logging_config import get_logger
# from src.utils.log_messages import (
#     upload_started,
#     upload_success,
#     upload_failed,
# )

# logger = get_logger(__name__)
# app = FastAPI()

# @app.post("/upload-repo")
# async def upload_repo(file: UploadFile = File(...)) -> JSONResponse:
#     with tempfile.TemporaryDirectory() as tmpdir:
#         repo_path: str = os.path.join(tmpdir, file.filename)
#         with open(repo_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         container_name: str = sanitize_container_name(os.path.splitext(file.filename)[0])
#         logger.info(upload_started(repo_path, container_name))
#         start_time: float = time.time()

#         try:
#             with BlobManager() as blob_manager:
#                 uploader: RepoUploader = RepoUploader(blob_manager, logger)
#                 total_files: int = uploader.upload_repository(tmpdir, container_name)

#             elapsed_time: float = time.time() - start_time
#             logger.info(upload_success(repo_path, total_files, elapsed_time))
#             return JSONResponse(status_code=200, content={
#                 "message": "Upload completed",
#                 "container": container_name,
#                 "elapsed_time": round(elapsed_time, 2)
#             })
#         except Exception as e:
#             elapsed_time: float = time.time() - start_time
#             logger.error(upload_failed(repo_path, elapsed_time, e))
#             raise HTTPException(status_code=500, detail="Upload failed")

import os
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from azure.storage.blob import ContainerClient

from src.services.blob_manager import BlobManager
from src.utils.helpers import sanitize_container_name

class RepoUploader:
    def __init__(self, blob_manager: BlobManager) -> None:
        self.blob_manager = blob_manager

    def __upload_file(self, container_client: ContainerClient, full_path: str, relative_path: str) -> None:
        blob_client = container_client.get_blob_client(relative_path)
        with open(full_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

    def upload_repository(self, repo_path: str, max_workers: int = 8) -> int:
        container_name: str = sanitize_container_name(os.path.basename(os.path.normpath(repo_path)))
        container_client: ContainerClient = self.blob_manager.ensure_container_exists(container_name)

        file_paths: List[Tuple[str, str]] = [
            (os.path.join(root, file), os.path.relpath(os.path.join(root, file), repo_path).replace("\\", "/"))
            for root, _, files in os.walk(repo_path)
            for file in files
        ]

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.__upload_file, container_client, full, rel)
                for full, rel in file_paths
            ]
            for future in as_completed(futures):
                future.result()

        return len(file_paths)


import os
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from azure.storage.blob import ContainerClient

from src.services.blob_manager import BlobManager
from src.utils.helpers import sanitize_container_name

class RepoUploader:
    def __init__(self, blob_manager: BlobManager) -> None:
        self.blob_manager = blob_manager

    def upload_repository(self, repo_path: str, max_workers: int = 8) -> int:
        container_name = sanitize_container_name(os.path.basename(os.path.normpath(repo_path)))
        container_client = self.blob_manager.ensure_container_exists(container_name)

        files: List[Tuple[str, str]] = []
        for root, _, filenames in os.walk(repo_path):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, repo_path).replace("\\", "/")
                files.append((full_path, relative_path))

        self._upload_files(container_client, files, max_workers)
        return len(files)

    def _upload_files(
        self,
        container_client: ContainerClient,
        files: List[Tuple[str, str]],
        max_workers: int
    ) -> None:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self._upload_single_file, container_client, full, rel)
                for full, rel in files
            ]
            for future in as_completed(futures):
                future.result()

    def _upload_single_file(self, container_client: ContainerClient, full_path: str, relative_path: str) -> None:
        blob_client = container_client.get_blob_client(relative_path)
        with open(full_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)



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

   
