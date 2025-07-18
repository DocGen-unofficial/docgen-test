from fastapi import APIRouter
from .service import access_container, get_file_from_container, get_files_by_type, get_container, blob_to_parquet, container_to_parquet
from pydantic import BaseModel

router = APIRouter(prefix="/v3", tags=["Integration Layer"])

@router.get("/access-container/{container_name}")   
async def is_container_accessible(container_name: str):
    """
    Controllo per verificare se il container è accessibile.
    Predisposta una struttura per gestire le risposte in caso di errori
    """ 
    accessible_container = await access_container(container_name)
    return {"Container accessible": accessible_container}

@router.get("/get-container/{container_name}")
async def download_container(container_name: str):
    """
    Recupera un container specifico.
    I file vengono salvati nella cartella outputs.
    """
    await get_container(container_name)
    return {"message": f"Container {container_name} downloaded to /app/outputs"}

@router.get("/get-specific-blob/{container_name}/{blob_name}")
async def get_specific_blob(container_name: str, blob_name: str = None):
    """
    Download di singolo blob da un container.
    NECESSARIO SPECIFICARE NOME DI ENTRAMBI
    I file vengono salvati nella cartella outputs.
    """ 
    await get_file_from_container(container_name, blob_name)
    return {"File": [blob_name]}

@router.get("/get-files-by-type/{container_name}/{file_extension}")
async def get_blobs_by_type(container_name: str, file_extension: str):
    """
    Download di blob con un'estensione specifica
    SPECIFICARE NOME CONTAINER ED ESTENSIONE
    """
    await get_files_by_type(container_name, file_extension)
    return {"message": f"Files with extension {file_extension} downloaded from {container_name}"}

@router.get("/transform-to-parquet/{container_name}/{blob_name}")
async def transform_blob_to_parquet(container_name, blob_name):
    
    output_path = f"/app/outputs/{blob_name}.parquet"
    await blob_to_parquet(container_name, blob_name)
    return {"message": f"Blob {blob_name} from container {container_name} transformed to Parquet format"}


class TransformRequest(BaseModel):
    container_name: str
    single_parquet: bool

@router.post("/transform-container-to-parquet")
async def transform_container_to_parquet(request: TransformRequest):
    await container_to_parquet(request.container_name, request.single_parquet)
    return {"message": f"Container {request.container_name} transformed to Parquet format"}