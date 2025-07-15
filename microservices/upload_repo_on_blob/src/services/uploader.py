import os
from src.services.blob_manager import BlobManager

class RepoUploader:
    def __init__(self, blob_manager: BlobManager):
        self.blob_manager = blob_manager

    def upload_repository(self, repo_path: str, container_name: str):
        container_client = self.blob_manager.get_container_client(container_name)

        for root, _, files in os.walk(repo_path):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, repo_path).replace("\\", "/")
                blob_client = container_client.get_blob_client(relative_path)

                with open(full_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)
                    print(f"  ↳ Uploaded: {relative_path}")
