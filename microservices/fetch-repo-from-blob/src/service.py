from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError, HttpResponseError, ServiceRequestError, ResourceExistsError
import os

connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
blob_service_client = BlobServiceClient.from_connection_string(connection_string)


def access_container(container_name):
    
    container_client = blob_service_client.get_container_client(container_name)
    try:
        container_client.get_container_properties()
        return {"status": True, "details": "Container is accessible"}
    except ResourceNotFoundError:
        return {"status": False, "details": "Container not found"}  
    except ClientAuthenticationError:
        return {"status": False, "details": "Authentication failed"}
    except HttpResponseError as e:
        return {"status": False, "details": f"HTTP error: {str(e)}"}
    except ServiceRequestError as e:
        return {"status": False, "details": f"Service request error: {str(e)}"}
    except ResourceExistsError as e:
        return {"status": False, "details": f"Resource already exists: {str(e)}"}
    except (ValueError, TypeError) as e:
        return {"status": False, "details": f"Value error: {str(e)}"}
    except Exception as e:
        return {"status": False, "details": f"An error occurred: {str(e)}"}

def get_files_from_container(container_name, blob_name):

    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    blob_data = blob_client.download_blob().readall()

    output_dir = "/app/outputs"
    output_path = os.path.join(output_dir, blob_name)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(blob_data)
    return {"status": True, "details": f"File {blob_name} downloaded successfully to {output_path}"}    

def download_files_by_type(container_name, file_extension):
    container_client = blob_service_client.get_container_client(container_name)
    downloaded_blobs = []

    for blob in container_client.list_blobs():
        if blob.name.endswith(file_extension):
            result = get_files_from_container(container_name, blob.name)
            if result["status"]:
                downloaded_blobs.append(blob.name)
    return {
        "status": True,
        "details": f"Downloaded {len(downloaded_blobs)} files with extension {file_extension}",
        "files": downloaded_blobs
    }