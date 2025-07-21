import requests
from typing import Optional, Dict, Any, Tuple, Union

def get_repo_status(endpoint_url: str) -> int:
    """
    Get the status code from a repository endpoint.

    Args:
        endpoint_url (str): The URL of the endpoint to check.

    Returns:
        int: The HTTP status code returned by the endpoint.
    """
    response = requests.get(endpoint_url)
    return response.status_code


def get_repo_url(endpoint_url: str, request_body: Dict[str, Any]) -> Optional[Union[str, Tuple[bool, str]]]:
    """
    Send a POST request to retrieve the repository path from the endpoint.

    Args:
        endpoint_url (str): The URL of the endpoint to call.
        request_body (Dict[str, Any]): The JSON body to send in the request.

    Returns:
        Optional[Union[str, Tuple[bool, str]]]:
            - The repository path (str) if successful.
            - (False, "No token") if the path is not found.
            - None if the request fails.
    """
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

def check_container_conenction() -> None:
    """
    Placeholder for checking container connection.

    Returns:
        None
    """
    pass