from azure.storage.blob.aio import BlobServiceClient
import pandas as pd
import os


connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
output_dir = os.path.abspath(output_dir)
os.makedirs(output_dir, exist_ok=True)


async def get_blob_from_container(container_name, blob_name):
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
    stream = await blob_client.download_blob()
    blob_data = await stream.readall()

    output_path = os.path.join(output_dir, blob_name)
    dir_path = os.path.dirname(output_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(blob_data)
    return {"status": True, "details": f"File {blob_name} downloaded successfully to {output_path}"}    

async def blob_to_parquet(container_name, blob_name):
    """
    Converte un blob in formato Parquet e lo salva nella cartella outputs.
    Args:
        container_name (str): Il nome del container contenente il blob.
        blob_name (str): Il nome del blob da convertire.
    Returns:
        parquet: il blob convertito in formato Parquet
    """

    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    stream = await blob_client.download_blob()
    blob_data = await stream.readall()
    try:
        content = blob_data.decode('utf-8')
    except Exception:
        content = str(blob_data)
    df = pd.DataFrame([{
        "name": blob_name,
        "content": content
    }])
    output_path = os.path.join(output_dir, f"{blob_name}.parquet")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path)
    return {"status": True, 
            "details": f"Blob {blob_name} converted to Parquet and saved to {output_path}",
            "parquet_path": output_path,
            "content": content
        }


