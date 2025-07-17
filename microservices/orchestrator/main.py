from source.apicalls import get_repo_url

endpoint_url = "http://localhost:8089/v1/download_repository"

json_request_body = {
  "repository": "https://github.com/EY-AI-Data-Cagliari/Azure-AI-102.git",
  "token": ""
}

if __name__ == "__main__":

    get_repo_url(endpoint_url, json_request_body)
