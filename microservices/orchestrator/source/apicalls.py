import requests



def get_repo_status(endpoint_url):
    response = requests.get(endpoint_url)
    return response.status_code


def get_repo_url(endpoint_url, request_body):

    response = requests.post(
        endpoint_url,
        json=request_body
    )
    if response.status_code != 200:
        print("Connection error:", response.status_code)
        print("Response:", response.text)
        return None
    else:
        if response.json().get("path"):
            return response.json().get("path")
    return False, "No token"

def check_container_conenction():
    pass