from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from source.container_services import access_container, get_files_by_type, get_container, container_to_parquet
from source.blob_services import get_blob_from_container, blob_to_parquet
from source.schemas import (
    BlobRequest, BlobDownloadResponse, BlobToParquetRequest, ContainerRequest, ContainerAccessResponse,
    ContainerDownloadResponse, FilesByTypeRequest, FilesByTypeResponse,
    ContainerToParquetRequest
)


router = APIRouter(prefix="/v3", tags=["Integration Layer"])

@router.post("/access-container/", response_model=ContainerAccessResponse)
async def is_container_accessible(request: ContainerRequest):
    """
    Controllo per verificare se il container è accessibile.
    Predisposta una struttura per gestire le risposte in caso di errori
    """ 
    return await access_container(request.container_name)

@router.post("/get-container/", response_model=ContainerDownloadResponse)
async def download_container(request: ContainerRequest):
    """
    Recupera un container specifico.
    I file vengono salvati nella cartella outputs.
    """
    return await get_container(request.container_name)

@router.post("/get-specific-blob/", response_model=BlobDownloadResponse)
async def get_specific_blob(request: BlobRequest):
    """
    Download di singolo blob da un container.
    NECESSARIO SPECIFICARE NOME DI ENTRAMBI
    I file vengono salvati nella cartella outputs.
    """ 
    await get_blob_from_container(request.container_name, request.blob_name)
    return {"File": [request.blob_name]}

@router.post("/get-files-by-type/", response_model=FilesByTypeResponse)
async def get_blobs_by_type(request: FilesByTypeRequest):
    """
    Download di blob con un'estensione specifica
    SPECIFICARE NOME CONTAINER ED ESTENSIONE
    """
    await get_files_by_type(request.container_name, request.file_extension)
    return {"message": f"Files with extension {request.file_extension} downloaded from {request.container_name}"}

@router.post("/transform-to-parquet/")
async def transform_blob_to_parquet(request: BlobToParquetRequest):
    """
    Converte un singolo blob in formato parquet e lo salva nella cartella outputs
    Args:
        request (BlobToParquetRequest): Richiesta contenente il nome del container e del blob.
    Returns:
        FileResponse: Risposta con il file Parquet convertito.
    """
    result = await blob_to_parquet(request.container_name, request.blob_name)
    parquet_path = result.get("parquet_path")
    return FileResponse(parquet_path, media_type="application/octet-stream", filename=f"{request.blob_name}.parquet")

@router.post("/transform-container-to-parquet/")
async def transform_container_to_parquet(request: ContainerToParquetRequest):
    """
    Converte tutti i blob di un container in formato Parquet e li salva nella cartella outputs.
    Nella richiesta e' possibile specificare la condizione single_parquet:
    - se True, viene creato un UNICO file Parquet con tutti i blob del container
    - se False, viene creato un file Parquet PER OGNI blob del container
    Args:
        request (ContainerToParquetRequest): Richiesta contenente il nome del container e il nome del file Parquet.
    Returns:
        JSONResponse: Risposta con lo stato della conversione e il percorso del file Parquet.
    """
    result = await container_to_parquet(request.container_name, request.single_parquet)
    parquet_path = result.get("parquet_path")
    return {
        "status": result["status"],
        "message": f"Container {request.container_name} converted to Parquet and saved to {parquet_path}",
        "parquet_path": parquet_path
    }
