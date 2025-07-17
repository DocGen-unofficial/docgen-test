def upload_started(repo_path: str, container: str) -> str:
    return f"Upload started: repo_path='{repo_path}', container='{container}'"

def upload_success(repo_path: str, total_files: int, duration: float) -> str:
    return f"Upload successful: {total_files} files from '{repo_path}' in {duration:.2f} seconds"

def upload_failed(repo_path: str, duration: float, error: Exception) -> str:
    return f"Upload failed: repo_path='{repo_path}' in {duration:.2f}s with error: {str(error)}"
