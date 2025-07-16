from fastapi import APIRouter
from .service import access_container, get_file_from_container, get_files_by_type

router = APIRouter()

@router.get("/access-container/{container_name}")   
def is_container_accessible(container_name: str):
    """
    Controllo per verificare se il container è accessibile.
    Predisposta una struttura per gestire le risposte in caso di errori
    """ 
    accessible_container = access_container(container_name)
    return {"Container accessible": accessible_container}

@router.get("/get-specific-blob/{container_name}/{blob_name}")
def get_specific_blob(container_name: str, blob_name: str = None):
    """
    Download di singolo blob da un container.
    NECESSARIO SPECIFICARE NOME DI ENTRAMBI
    I file vengono salvati nella cartella outputs.
    """ 
    get_file_from_container(container_name, blob_name)
    return {"File": [blob_name]}

@router.get("/get-files-by-type/{container_name}/{file_extension}")
def get_blobs_by_type(container_name: str, file_extension: str):
    """
    Download di blob con un'estensione specifica
    SPECIFICARE NOME CONTAINER ED ESTENSIONE
    """
    get_files_by_type(container_name, file_extension)
    return {"message": f"Files with extension {file_extension} downloaded from {container_name}"}