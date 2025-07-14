from azure.storage.blob import BlobServiceClient
import os

def download_blobs(container_name, directory):

    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    os.makedirs(directory, exist_ok=True)

    for blob in container_client.list_blobs():
        with open(os.path.join(directory, blob.name), "wb") as f:
            f.write(container_client.download_blob(blob).readall())


if __name__ == "__main__":
    download_blobs("your-container-name", "local-directory")