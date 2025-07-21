import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Configuration class for accessing Azure Blob Storage.

    Args:
        CONNECTION_STRING (str): Connection string for Azure Blob Storage.
            Retrieved from the environment variable 'AZURE_STORAGE_CONNECTION_STRING'.
    """
    CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
