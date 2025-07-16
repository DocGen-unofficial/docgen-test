import os
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

class RepoUploader:
    def __init__(self, blob_manager):
        self.blob_manager = blob_manager

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    async def upload_file_async(self, container_client, full_path, relative_path):
        blob_client = container_client.get_blob_client(relative_path)
        with open(full_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

    async def upload_repository_async(self, repo_path: str, container_name: str) -> int:
        container_client = self.blob_manager.ensure_container_exists(container_name)
        tasks = []
        file_count = 0

        for root, _, files in os.walk(repo_path):
            for file in files:
                file_count += 1
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, repo_path).replace("\\", "/")
                task = asyncio.create_task(
                    self.upload_file_async(container_client, full_path, relative_path)
                )
                tasks.append(task)

        await asyncio.gather(*tasks)
        return file_count
