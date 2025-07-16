def upload_started(local_path: str, container_name: str) -> str:
    return f"Upload started: repo='{local_path}', container='{container_name}'"

def upload_success(local_path: str, total_files: int, elapsed_time: float) -> str:
    return (f"Upload completed successfully for '{local_path}' "
            f"(uploaded {total_files} files in {elapsed_time:.2f} seconds).")

def upload_failed(local_path: str, elapsed_time: float, error: Exception) -> str:
    return (f"Upload failed after {elapsed_time:.2f} seconds for '{local_path}': {error}")
