import pandas as pd
from typing import List, Dict, Optional
from pydantic import BaseModel, validator, FilePath
import re
from pathlib import Path


class TextCleaner:
    """
    Class to load a parquet file and extract .txt file contents
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the class with the DataFrame to extract

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the data to extract
        """
        self.df = df

    
    def __remove_extra_whitespace(self, text: str) -> str:
        """
        Remove multiple spaces, tabs and excessive newlines
        
        Parameters
        ----------
        text : str
            Text to clean
            
        Returns
        -------
        str
            Text with normalized whitespace
        """
        # Replace tabs with spaces
        text = text.replace('\t', ' ')
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        # Remove multiple newlines with single one
        text = re.sub(r'\n+', '\n', text)
        # Remove spaces before and after newlines
        text = re.sub(r' *\n *', '\n', text)
        return text.strip()
    
    def __remove_special_characters(self, text: str) -> str:
        """
        Remove unnecessary special characters from text
        
        Parameters
        ----------
        text : str
            Text to clean
            
        Returns
        -------
        str
            Text with special characters removed
        """
        # Keep only letters, numbers, spaces, basic punctuation and HTML tags
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\{\}\"\'\/\n<>]', ' ', text)
        return text
    
    def __normalize_punctuation(self, text: str) -> str:
        """
        Normalize punctuation spacing
        
        Parameters
        ----------
        text : str
            Text to normalize
            
        Returns
        -------
        str
            Text with normalized punctuation
        """
        # Add space after punctuation if missing
        text = re.sub(r'([.!?,;:])([A-Za-z])', r'\1 \2', text)
        # Remove spaces before punctuation
        text = re.sub(r'\s+([.!?,;:])', r'\1', text)
        return text
    
    def __remove_urls(self, text: str) -> str:
        """
        Remove URLs from text
        
        Parameters
        ----------
        text : str
            Text containing URLs
            
        Returns
        -------
        str
            Text with URLs removed
        """
        # Remove http/https URLs
        text = re.sub(r'https?://\S+', '', text)
        # Remove www URLs
        text = re.sub(r'www\.\S+', '', text)
        return text
    
    def __remove_emails(self, text: str) -> str:
        """
        Remove email addresses
        
        Parameters
        ----------
        text : str
            Text containing email addresses
            
        Returns
        -------
        str
            Text with email addresses removed
        """
        text = re.sub(r'\S+@\S+', '', text)
        return text
    
    def __fix_encoding_issues(self, text: str) -> str:
        """
        Fix common encoding issues
        
        Parameters
        ----------
        text : str
            Text with potential encoding issues
            
        Returns
        -------
        str
            Text with encoding issues fixed
        """
        # Replace common malformed encoding characters
        replacements = {
            'â€™': "'",
            'â€œ': '"',
            'â€': '"',
            'â€"': '-',
            'â€"': '—',
            'Ã©': 'é',
            'Ã¨': 'è',
            'Ã ': 'à',
            'Ã¹': 'ù',
            'Ã²': 'ò',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    def __lowercase_text(self, text: str) -> str:
        """
        Convert text to lowercase
        
        Parameters
        ----------
        text : str
            Text to convert
            
        Returns
        -------
        str
            Lowercase text
        """
        return text.lower()
    
    def __remove_short_lines(self, text: str) -> str:
        """
        Remove lines that are too short (less than 3 characters)
        
        Parameters
        ----------
        text : str
            Text with multiple lines
            
        Returns
        -------
        str
            Text with short lines removed
        """
        lines = text.split('\n')
        lines = [line for line in lines if len(line.strip()) > 2]
        return '\n'.join(lines)
    
    def clean_text(self, text: str) -> str:
        """
        Main method that calls all cleaning methods in sequence
        
        Parameters
        ----------
        text : str
            Text to clean
            
        Returns
        -------
        str
            Cleaned text ready for chunking and embedding
        """
        text = self.__fix_encoding_issues(text)
        text = self.__remove_urls(text)
        text = self.__remove_emails(text)
        text = self.__remove_special_characters(text)
        text = self.__normalize_punctuation(text)
        text = self.__remove_extra_whitespace(text)
        text = self.__lowercase_text(text)
        text = self.__remove_short_lines(text)
        return text
    
    def get_txt_files(self) -> Dict[str, str]:
        """
        Identify files with .txt extension and return a dictionary
        with filename and content
        
        Returns
        -------
        Dict[str, str]
            Dictionary with key=filename, value=content
        """
        if self.df is None or self.df.empty:
            return {}
        
        # Assume the first column contains filenames and the second contains content
        file_col = self.df.iloc[:, 0]
        content_col = self.df.iloc[:, 1]
        
        txt_files = {}
        
        for idx, filename in enumerate(file_col):
            # Check if file has .txt extension and is not requirements.txt
            if str(filename).lower().endswith('.txt') and not str(filename).lower().endswith('requirements.txt'):
                raw_content = str(content_col.iloc[idx])
                cleaned_content = self.clean_text(raw_content)
                txt_files[str(filename)] = cleaned_content
        
        return txt_files
    
    def get_txt_files_as_list(self) -> List[tuple]:
        """
        Return a list of tuples (filename, content) for .txt files
        
        Returns
        -------
        List[tuple]
            List of tuples with (filename, content)
        """
        txt_dict = self.get_txt_files()
        return [(name, content) for name, content in txt_dict.items()]
    
    def save_cleaned_df(self) -> None:
        """
        Save updated DataFrame with cleaned content to a new parquet file
        
        Parameters
        ----------
        output_path : str
            Path where to save the output parquet file
        """
        if self.df is None or self.df.empty:
            raise ValueError("No data to save")
        
        # Create a copy of the dataframe
        df_cleaned = self.df.copy()
        
        # Clean content for .txt files directly in second column
        for idx in range(len(df_cleaned)):
            filename = str(df_cleaned.iloc[idx, 0])
            if filename.lower().endswith('.txt') and not filename.lower().split("/")[-1] == 'requirements.txt':
                raw_content = str(df_cleaned.iloc[idx, 1])
                cleaned = self.clean_text(raw_content)
                df_cleaned.iloc[idx, 1] = cleaned
        
        # Save to parquet
        return df_cleaned