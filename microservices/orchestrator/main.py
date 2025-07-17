from source.apicalls import get_repo_url

endpoint_url = "http://localhost:8081/v1/download_repository"

json_request_body = {
  "repository": "https://github.com/chrisputzu/docgentest_private_repo.git",
  "token": ""
}

if __name__ == "__main__":

    print(get_repo_url(endpoint_url, json_request_body))
