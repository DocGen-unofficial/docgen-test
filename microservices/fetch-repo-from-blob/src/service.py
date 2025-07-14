from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
import os

def is_valid_blob(blob_name, blob_data, min_size):
    if len(blob_data) < min_size:
        print(f"Blob {blob_name} is too small.")
        return False
    return True

def is_blob_accessible(container_name):
    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    container_client = BlobServiceClient.from_connection_string(connection_string)
    try:
        container_client.get_container_properties(container_name)
        return True
    except ResourceNotFoundError:
        print(f"Container {container_name} does not exist.")
        return False
    
def download_and_validate_blobs(container_name):

    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    for blob in container_client.list_blobs():
        blob_client = container_client.get_blob_client(blob)
        blob_data = blob_client.download_blob().readall()
        if is_valid_blob(blob.name, blob_data):
            print(f"Valid blob: {blob.name}")
            # processing logic
        else:
            print(f"Invalid blob: {blob.name}")


if __name__ == "__main__":
    
    download_and_validate_blobs("your-container-name")