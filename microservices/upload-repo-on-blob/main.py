import os
import re
import sys
from src.services.blob_manager import BlobManager
from src.services.uploader import RepoUploader

def sanitize_container_name(name: str) -> str:
    name = name.lower()
    name = re.sub(r'[^a-z0-9-]', '-', name)
    name = re.sub(r'-+', '-', name).strip('-')
    if len(name) >= 3 and len(name) <= 22:
        return name
    elif len(name) > 24:
        return name[:22]
    else:
        return f"repo-{name}"

def main():
    local_path = r"microservices\upload-repo-on-blob\UnicAssistant4554"
    repo_name = os.path.basename(os.path.normpath(local_path))
    print(repo_name)
    container_name = sanitize_container_name(repo_name)
    print(container_name)

    print(f"[•] Uploading repo '{repo_name}' from '{local_path}' to container '{container_name}'...")

    blob_manager = BlobManager()
    if blob_manager.ensure_container_exists(container_name):
        uploader = RepoUploader(blob_manager)
        uploader.upload_repository(local_path, container_name)
        print(f"[✔] Upload complete for repo '{repo_name}'.")
    else:
        print(f"[i] Container '{container_name}' already exists. Skipping creation.")

if __name__ == "__main__":
    main()
