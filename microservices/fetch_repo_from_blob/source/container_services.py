import os
import logging
from dotenv import load_dotenv
import pandas as pd
from azure.storage.blob.aio import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError, HttpResponseError, ServiceRequestError, ResourceExistsError
from source.blob_services import get_blob_from_container, blob_to_parquet
load_dotenv()
from utilities.retry import azure_retry
from utilities.chunk_rows import chunk_rows

logger = logging.getLogger(__name__)

connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
output_dir = os.path.abspath(output_dir)
os.makedirs(output_dir, exist_ok=True)

@azure_retry
async def access_container(container_name):
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
        await container_client.get_container_properties()
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

@azure_retry
async def get_container(container_name):
    """
    Recupera un container specifico.
    Args:
        container_name (str): Il nome del container da recuperare.
    Returns:
        folder: il container specificato.
    """
    container_client = blob_service_client.get_container_client(container_name)
    downloaded_blobs = []
    async for blob in container_client.list_blobs():
        blob_client = container_client.get_blob_client(blob.name)
        stream = await blob_client.download_blob()
        blob_data = await stream.readall()
        output_path = os.path.join(output_dir, blob.name)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f: 
            f.write(blob_data)
        downloaded_blobs.append(blob.name)
    
    return {
        "status": True,
        "details": f"Downloaded {len(downloaded_blobs)} blobs from container {container_name}",
        "files": downloaded_blobs
    }

@azure_retry
async def get_files_by_type(container_name, file_extension):
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

    async for blob in container_client.list_blobs():
        if blob.name.endswith(file_extension):
            result = await get_blob_from_container(container_name, blob.name)
            if result["status"]:
                downloaded_blobs.append(result)
    return {
        "status": True,
        "details": f"Downloaded {len(downloaded_blobs)} files with extension {file_extension}",
        "files": downloaded_blobs
    }

@azure_retry
async def container_to_parquet(container_name, single_parquet=False):
    """
    Converte un container in formato Parquet e lo salva nella cartella outputs.
    Args:
        container_name (str): Il nome del container contenente il blob.
        blob_name (str): Il nome del blob da convertire.
    Returns:
        parquet: il container convertito in formato Parquet
    """
    container_client = blob_service_client.get_container_client(container_name)
    
    os.makedirs(output_dir, exist_ok=True)
    if single_parquet:
        rows = []
        async for blob in container_client.list_blobs():
            blob_client = container_client.get_blob_client(blob.name)
            stream = await blob_client.download_blob()
            blob.data = await stream.readall()
            try:
                content = blob.data.decode('utf-8')
            except Exception:
                content = str(blob.data)
            rows.append({
                "name": blob.name,
                "content": content
            })
        chunk_size = 1000000
        parquet_path = []
        for idx, chunk in enumerate(chunk_rows(rows, chunk_size)):
            df = pd.DataFrame(chunk)
            output_path = os.path.join(output_dir, f"{container_name}_part_{idx}.parquet")
            df.to_parquet(output_path)
            parquet_path.append(output_path)
        return {
            "status": True,
            "details": f"Container {container_name} converted to Parquet and saved to {output_path}",
            "parquet_path": output_path,
            "files": [{"name": container_name, "content": content}]
        }
    else:
        files = []
        async for blob in container_client.list_blobs():
            result = await blob_to_parquet(container_name, blob.name)
            if result["status"]:
                files.append(result)
        return {
            "status": True,
            "details": f"Converted {len(files)} blobs in container {container_name} to Parquet",
            "files": files
        }
    


# aggiungere controllo file per verificare se convertibile e inseribile su parquet???