from source.apicalls import get_repo_url
import requests

json_request_body = {
  "repository": "https://github.com/EY-AI-Data-Cagliari/Azure-AI-102.git",
  "token": ""
}

if __name__ == "__main__":

    response = requests.post("http://localhost:5001/v1/download_repository", 
                             json=json_request_body)
    
    print("1 step finito")
    
    response = requests.post("http://localhost:5002/v2/repo/upload", 
                             params={"repo_path": response.json()["path"]})
    
    print(response.json())
    container = response.json()["container_name"]

    print("2 step finito")

    response = requests.post("http://localhost:5003/v3/transform-container-to-parquet",
                            json={'container_name': container, 'single_parquet': True})
    
    print(response.json()["message"])