from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
from source.text_cleaning_services import clean_parquet_file, validate_parquet_file
from source.schemas import CleanParquetResponse, ValidationResponse, HealthResponse
import os
import tempfile
from datetime import datetime

router = APIRouter(prefix="/v1", tags=["Text Cleaning"])

@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check():
    """
    Check if the service is alive and running.
    Returns service status and timestamp.
    """
    return {
        "status": "healthy",
        "service": "Text Cleaning API",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@router.post("/validate-parquet/", response_model=ValidationResponse, status_code=status.HTTP_200_OK)
async def validate_parquet(file: UploadFile = File(...)):
    """
    Validate if the uploaded file is a valid parquet file with expected structure.
    Returns validation status and file metadata.
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".parquet") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Validate the file
        result = await validate_parquet_file(tmp_file_path)
        
        # Clean up
        os.unlink(tmp_file_path)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/clean-parquet/", response_model=CleanParquetResponse, status_code=status.HTTP_200_OK)
async def clean_parquet(output_filename: str, file: UploadFile = File(...)):
    """
    Clean text content in parquet file for .txt files (excluding requirements.txt).
    Preserves HTML structure and returns cleaned parquet file.
    """
    try:
        # Validate output filename
        if not output_filename.endswith('.parquet'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Output filename must have .parquet extension"
            )
        if '/' in output_filename or '\\' in output_filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Output filename cannot contain path separators"
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".parquet") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Process the file
        result = await clean_parquet_file(tmp_file_path, output_filename)
        
        # Clean up input file
        os.unlink(tmp_file_path)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/download-cleaned/{filename}", status_code=status.HTTP_200_OK)
async def download_cleaned_file(filename: str):
    """
    Download the cleaned parquet file from outputs directory.
    """
    file_path = os.path.join("outputs", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    return FileResponse(
        file_path, 
        media_type="application/octet-stream", 
        filename=filename
    )