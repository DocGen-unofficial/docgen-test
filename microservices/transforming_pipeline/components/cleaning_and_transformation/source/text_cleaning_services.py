import os
import pandas as pd
from typing import Dict
from AIDocGen.microservices.transforming_pipeline.components.cleaning_and_transformation.source.text_cleaner import ParquetTxtExtractor

async def validate_parquet_file(file_path: str) -> Dict:
    """
    Validate parquet file structure and content
    
    Parameters
    ----------
    file_path : str
        Path to the parquet file to validate
        
    Returns
    -------
    Dict
        Validation results
    """
    try:
        # Read parquet file
        df = pd.read_parquet(file_path)
        
        # Check if file has at least 2 columns
        if df.shape[1] < 2:
            return {
                "is_valid": False,
                "columns": list(df.columns),
                "row_count": len(df),
                "txt_file_count": 0,
                "message": "Parquet file must have at least 2 columns"
            }
        
        # Count .txt files
        txt_count = df.iloc[:, 0].astype(str).str.lower().str.endswith('.txt').sum()
        
        return {
            "is_valid": True,
            "columns": list(df.columns),
            "row_count": len(df),
            "txt_file_count": int(txt_count),
            "message": "Parquet file is valid and ready for processing"
        }
    except Exception as e:
        return {
            "is_valid": False,
            "columns": [],
            "row_count": 0,
            "txt_file_count": 0,
            "message": f"Error validating file: {str(e)}"
        }

async def clean_parquet_file(input_path: str, output_filename: str) -> Dict:
    """
    Clean text content in parquet file
    
    Parameters
    ----------
    input_path : str
        Path to the input parquet file
    output_filename : str
        Name for the output file
        
    Returns
    -------
    Dict
        Processing results
    """
    try:
        # Ensure outputs directory exists
        os.makedirs("outputs", exist_ok=True)
        
        # Initialize extractor
        extractor = ParquetTxtExtractor(input_path)
        
        # Get initial stats
        df = extractor.df
        total_files = len(df)
        txt_files = df.iloc[:, 0].astype(str).str.lower().str.endswith('.txt').sum()
        requirements_files = df.iloc[:, 0].astype(str).str.lower().str.endswith('requirements.txt').sum()
        txt_files_to_clean = txt_files - requirements_files
        
        # Process and save
        output_path = os.path.join("outputs", output_filename)
        extractor.save_cleaned_parquet(output_path)
        
        return {
            "status": "success",
            "message": f"Successfully cleaned {txt_files_to_clean} .txt files",
            "output_path": output_path,
            "files_processed": total_files,
            "txt_files_cleaned": int(txt_files_to_clean)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error processing file: {str(e)}",
            "output_path": "",
            "files_processed": 0,
            "txt_files_cleaned": 0
        }