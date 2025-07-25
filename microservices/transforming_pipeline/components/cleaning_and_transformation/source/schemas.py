from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str = Field(..., description="Service health status")
    service: str = Field(..., description="Service name")
    timestamp: str = Field(..., description="Current timestamp in ISO format")
    version: str = Field(..., description="API version")

class CleanParquetResponse(BaseModel):
    """Response model for parquet cleaning operation"""
    status: str = Field(..., description="Operation status", example="success")
    message: str = Field(..., description="Descriptive message", example="Successfully cleaned 5 .txt files")
    output_path: str = Field(..., description="Path to the cleaned parquet file", example="outputs/cleaned_data.parquet")
    files_processed: int = Field(..., description="Number of files processed", ge=0)
    txt_files_cleaned: int = Field(..., description="Number of .txt files cleaned", ge=0)

class ValidationResponse(BaseModel):
    """Response model for parquet validation"""
    is_valid: bool = Field(..., description="Whether the parquet file is valid")
    columns: List[str] = Field(..., description="Column names in the parquet file")
    row_count: int = Field(..., description="Number of rows in the parquet file", ge=0)
    txt_file_count: int = Field(..., description="Number of .txt files found", ge=0)
    message: str = Field(..., description="Validation message")

class ErrorResponse(BaseModel):
    """Response model for error cases"""
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Detailed error message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }