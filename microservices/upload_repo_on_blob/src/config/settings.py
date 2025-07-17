import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    # AUTH_MODE = os.getenv("AZURE_AUTH_MODE", "connection_string")
    # STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")

