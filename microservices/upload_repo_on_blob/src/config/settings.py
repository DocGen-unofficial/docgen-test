import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")


