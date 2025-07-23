from source.apicalls import get_repo_url
import requests

json_request_body: dict = {
  "repository": "https://github.com/DocGen-unofficial/docgen-test.git",
  "token": ""
}

if __name__ == "__main__":
    """
    Main orchestrator script for coordinating the download, upload, and transformation of a GitHub repository.

    Attributes:
        json_request_body (dict): The request body containing the repository URL and optional token.

    Workflow:
        1. Sends a POST request to the repo_downloader microservice to download a repository.
        2. Sends a POST request to the uploader microservice to upload the repository to blob storage.
        3. Sends a POST request to the transformer microservice to convert the repository to Parquet format.

    Usage:
        Run as a script. The script will print the status of each step.
    """
    response = requests.post("http://localhost:5001/v1/download_repository", 
                             json=json_request_body)
    
    print("1 step finito")
    
    response = requests.post("http://localhost:5002/v2/repo/upload", 
                             params={"repo_path": response.json()["path"]})
    
    print(response.json())
    container: str = response.json()["container_name"]

    print("2 step finito")

    response = requests.post("http://localhost:5003/v3/transform-container-to-parquet",
                            json={'container_name': container, 'single_parquet': True})
    
    print(response.json()["message"], response.json()["parquet_path"])