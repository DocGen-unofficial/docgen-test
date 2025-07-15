import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # AUTH_MODE = os.getenv("AZURE_AUTH_MODE", "connection_string")
    CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    # STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")

