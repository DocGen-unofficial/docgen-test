import os
import asyncio
import time

from src.services.blob_manager import BlobManager
from src.services.uploader import RepoUploader
from src.utils.helpers import sanitize_container_name
from src.utils.logging_config import get_logger
from src.utils.log_messages import (
    upload_started,
    upload_success,
    upload_failed,
)

logger = get_logger(__name__)

async def process_repo_upload(local_path: str) -> str:
    container_name = sanitize_container_name(os.path.basename(local_path))

    logger.info(upload_started(local_path, container_name))
    start_time = time.time()

    with BlobManager() as blob_manager:
        uploader = RepoUploader(blob_manager)
        try:
            total_files = await uploader.upload_repository_async(local_path, container_name)
            elapsed_time = time.time() - start_time
            logger.info(upload_success(local_path, total_files, elapsed_time))
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(upload_failed(local_path, elapsed_time, e))
            raise e

    return container_name

if __name__ == "__main__":
    test_repo_path = r"C:\VS Project\docgen-test\microservices\upload-repo-on-blob\UnicAssistant"
    asyncio.run(process_repo_upload(test_repo_path))
