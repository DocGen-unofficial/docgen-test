import re
import uuid

def sanitize_container_name(name: str) -> str:
    """
    Sanitizes a string to produce a valid Azure Blob Storage container name.

    Rules enforced:
    - Must be between 3 and 63 characters long.
    - Must contain only lowercase letters, numbers, and hyphens.
    - Must begin and end with a letter or a number.
    - Hyphens must be surrounded by letters or numbers (no leading/trailing hyphens, no consecutive hyphens).

    If the cleaned name does not meet these criteria, a fallback UUID-based name is generated.

    Args:
        name (str): The input string, typically a folder or repository name.

    Returns:
        str: A valid Azure container name.
    """
    name = re.sub(r'[^a-z0-9-]', '-', name.lower())
    name = re.sub(r'-{2,}', '-', name)
    name = name.strip('-')
    name = name[:63].strip('-')  

    return name 
