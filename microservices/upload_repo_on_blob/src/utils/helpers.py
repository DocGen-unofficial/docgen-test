import re

def sanitize_container_name(name: str) -> str:
    name = name.lower()
    name = re.sub(r'[^a-z0-9-]', '-', name)
    name = re.sub(r'-+', '-', name).strip('-')

    if len(name) < 3:
        return f"repo-{name}".ljust(3, 'x')[:3]
    elif len(name) > 24:
        return name[:24]
    return name
