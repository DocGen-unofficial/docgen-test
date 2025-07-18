from source.apicalls import get_repo_url
import requests

endpoint_url = "http://localhost:5001/v1/download_repository"

json_request_body = {
  "repository": "https://github.com/EY-AI-Data-Cagliari/Azure-AI-102.git",
  "token": ""
}

if __name__ == "__main__":

    response = requests.post(endpoint_url, json=json_request_body)
    print(f"Status: {response.status_code}")
