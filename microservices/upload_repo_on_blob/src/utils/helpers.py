import re

def sanitize_container_name(name: str) -> str:
    name = name.lower()
    name = re.sub(r'[^a-z0-9-]', '-', name)
    name = re.sub(r'-+', '-', name).strip('-')
    if 3 <= len(name) <= 22:
        return name
    elif len(name) > 24:
        return name[:22]
    else:
        return f"repo-{name}"
