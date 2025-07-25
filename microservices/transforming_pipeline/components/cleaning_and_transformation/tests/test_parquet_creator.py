import pandas as pd
import os
from pathlib import Path


def create_test_parquet(txt_file_path: str, output_parquet_path: str):
    """
    Create a parquet file from a text file for testing purposes
    
    Parameters
    ----------
    txt_file_path : str
        Path to the input text file
    output_parquet_path : str
        Path where to save the output parquet file
    """
    # Check if file exists
    if not os.path.exists(txt_file_path):
        raise FileNotFoundError(f"File not found: {txt_file_path}")
    
    # Read the content of the text file
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get the filename from the path
    filename = os.path.basename(txt_file_path)
    
    # Create a DataFrame with two columns
    df = pd.DataFrame({
        'filename': [filename],
        'content': [content]
    })
    
    # Save as parquet
    df.to_parquet(output_parquet_path, index=False)
    print(f"Parquet file created successfully: {output_parquet_path}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"File processed: {filename}")
    print(f"Content length: {len(content)} characters")


if __name__ == "__main__":
    # Paths for test files
    local_dir = Path(__file__).parent
    input_txt = local_dir / "code_explanation.txt"  # The text file you downloaded
    output_parquet = local_dir / "test_data.parquet"
    
    try:
        # Create the test parquet file
        create_test_parquet(input_txt, output_parquet)
        
        # Verify by reading back
        print("\nVerifying created parquet file:")
        df_verify = pd.read_parquet(output_parquet)
        print(f"Verified shape: {df_verify.shape}")
        print(f"First 100 characters of content: {df_verify.iloc[0, 1][:100]}...")
        
    except Exception as e:
        print(f"Error: {e}")