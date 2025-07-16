from azure.storage.blob import BlobServiceClient
from src.config.settings import Settings
from dotenv import load_dotenv
load_dotenv()

class BlobManager:
    def __init__(self):
        if not Settings.CONNECTION_STRING:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING must be set in the environment.")
        
        self.service_client = BlobServiceClient.from_connection_string(Settings.CONNECTION_STRING)
        print(self.service_client)

    def ensure_container_exists(self, container_name: str)-> bool:
        container_client = self.service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
            print(f"[✔] Container '{container_name}' created.")
            return True
        else:
            print(f"[i] Container '{container_name}' already exists.")
            return False
        
    def get_container_client(self, container_name: str):
        return self.service_client.get_container_client(container_name)
