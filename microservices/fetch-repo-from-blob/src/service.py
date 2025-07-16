import os
import logging
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError, HttpResponseError, ServiceRequestError, ResourceExistsError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
blob_service_client = BlobServiceClient.from_connection_string(connection_string)


def access_container(container_name):
    """
    Controllo per verificare se il container è accessibile.
    Sarebbe da eseguire come primo check prima di qualsiasi operazione sui blob.
    Arg:
        container_name (str): Il nome del container da verificare.

    Returns:
        dict: Un dizionario con lo stato dell'accessibilità del container e eventuali dettagli sugli errori.
    """
    container_client = blob_service_client.get_container_client(container_name)
    try:
        container_client.get_container_properties()
        return {"status": True, "details": "Container is accessible"}
    except ResourceNotFoundError:
        logger.error("Container not found: %s", container_name)
        return {"status": False, "details": "Container not found"}  
    except ClientAuthenticationError:
        logger.error("Authentication failed for container: %s", container_name)
        return {"status": False, "details": "Authentication failed"}
    except HttpResponseError as e:
        logger.error("HTTP error occurred: %s", str(e))
        return {"status": False, "details": f"HTTP error: {str(e)}"}
    except ServiceRequestError as e:
        logger.error("Service request error occurred: %s", str(e))
        return {"status": False, "details": f"Service request error: {str(e)}"}
    except ResourceExistsError as e:
        return {"status": False, "details": f"Resource already exists: {str(e)}"}
    except (ValueError, TypeError) as e:
        logger.error("Value or Type error occurred: %s", str(e))
        return {"status": False, "details": f"Value error: {str(e)}"}
    except Exception as e:
        logger.error("An error occurred: %s", str(e))
        return {"status": False, "details": f"An error occurred: {str(e)}"}



def get_file_from_container(container_name, blob_name):
    """
    Recupera un singolo blob da un container e lo salva nella cartella outputs.
    Args:
        container_name (str): Il nome del container da cui scaricare il blob.
        blob_name (str): Il nome del blob da scaricare.
    Returns:
        dict: Un dizionario con lo stato del download e i dettagli del file scaricato.
        file: il blob selezionato viene salvato nella cartella
    """
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    blob_data = blob_client.download_blob().readall()

    output_dir = "/app/outputs"
    output_path = os.path.join(output_dir, blob_name)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(blob_data)
    return {"status": True, "details": f"File {blob_name} downloaded successfully to {output_path}"}    



def get_files_by_type(container_name, file_extension):
    """
    Recupera tutti i blob di un container con un'estensione specifica e li salva nella cartella outputs.
    Args:
        container_name (str): Il nome del container da cui scaricare i blob.
        file_extension (str): L'estensione dei file da scaricare.
    Returns:
        dict: Un dizionario con lo stato del download e i dettagli dei file scaricati.
    """
    container_client = blob_service_client.get_container_client(container_name)
    downloaded_blobs = []

    for blob in container_client.list_blobs():
        if blob.name.endswith(file_extension):
            result = get_file_from_container(container_name, blob.name)
            if result["status"]:
                downloaded_blobs.append(blob.name)
    return {
        "status": True,
        "details": f"Downloaded {len(downloaded_blobs)} files with extension {file_extension}",
        "files": downloaded_blobs
    }



# downloading in async controllare