# Repo Downloader Microservice

A FastAPI-based microservice for cloning GitHub repositories, supporting both public and private repositories with authentication.

## Overview

This microservice provides REST API endpoints to clone GitHub repositories to the local filesystem. It includes validation of GitHub URLs, support for private repositories with access tokens, and health check functionality.

## Architecture & Workflow

### System Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client        │───▶│  FastAPI Server  │───▶│  GitHub Cloner  │
│   (HTTP Request)│    │  (Port 8081)     │    │  (Local FS)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Response        │
                       │  (JSON)          │
                       └──────────────────┘
```

### Request Flow
1. **Client Request**: HTTP POST to `/v1/download_repository`
2. **API Validation**: Pydantic model validates request data
3. **URL Validation**: Regex pattern validates GitHub URL format
4. **Authentication**: Token added to URL for private repos
5. **Git Clone**: Repository cloned to local filesystem
6. **Response**: Success/error status returned to client

### Deployment Architecture
- **Container**: Docker container with Python 3.11-slim
- **Port**: 8081 (configurable)
- **SSL**: Disabled for corporate environments
- **CORS**: Enabled for cross-origin requests

### Containerization & Orchestration

#### Dockerfile
The Dockerfile is essential for containerizing the microservice and managing it at the pipeline and orchestrator level:

**Key Features:**
- **Base Image**: Python 3.11-slim for optimized container size
- **Git Installation**: Installs Git for repository cloning operations
- **SSL Configuration**: Disables SSL verification for corporate environments
- **Dependency Management**: Installs Python dependencies from requirements.txt
- **Port Exposure**: Exposes port 8081 for API access

## Features

- **GitHub Repository Cloning**: Clone public and private repositories
- **Authentication Support**: Private repository access with GitHub tokens
- **URL Validation**: Automatic validation of GitHub repository URLs
- **Health Check**: API status monitoring endpoint
- **Docker Support**: Containerized deployment
- **Test Coverage**: Comprehensive test suite

## API Endpoints

### Health Check
```http
GET /v1/status
```
Returns the API health status.

**Response:**
```json
{
  "message": "Ok"
}
```

### Repository Download
```http
POST /v1/download_repository
```

**Request Body:**
```json
{
  "repository": "https://github.com/owner/repo.git",
  "token": "ghp_your_github_token_here"  // Optional for private repos
}
```

**Response (Success):**
```json
{
  "message": "Repository successfully cloned.",
  "path": "/app/outputs/repo-name",
  "Url": "https://github.com/owner/repo.git"
}
```

**Response (Error):**
```json
{
  "message": "Link to repository invalid or not found"
}
```

### Core Components

- **`main.py`**: FastAPI application entry point with CORS middleware
- **`source/github_cloner.py`**: Core repository cloning logic with `DownloadRepo` class
- **`endpoints/`**: API route definitions
  - `status.py`: Health check endpoint (`GET /v1/status`)
  - `repo_download_api.py`: Repository download endpoint (`POST /v1/download_repository`)
- **`tests/`**: Comprehensive test suite covering URL validation, API connectivity, and repository cloning

## Micro-service Structure

```
repo_downloader/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration for pipeline/orchestration
├── README.md              # Project documentation
├── source/                # Core business logic
│   ├── __init__.py
│   └── github_cloner.py   # Repository cloning logic
├── endpoints/             # API route definitions
│   ├── status.py          # Health check endpoint
│   └── repo_download_api.py # Repository download endpoint
└── tests/                 # Test suite
    ├── __init__.py
    └── test_repo_downloader.py
```

### Key Classes

#### `DownloadRepo`
Main class for repository cloning operations:

**Methods:**
- `__init__(url_repository: str, token: Optional[str] = None)`: Initialize with repository URL and optional token
- `__check_url() -> None`: Validates GitHub URL using regex pattern
- `__add_token() -> None`: Adds authentication token to URL for private repos
- `__is_git_cloned() -> str`: Returns the local path where repository is stored
- `download() -> Tuple[bool, Optional[str], Optional[str]]`: Clones repository and returns success status, path, and URL

**Features:**
- URL validation using regex patterns
- Token-based authentication for private repos
- Local filesystem management
- Error handling and status reporting

#### `InvalidLinkRepository`
Custom exception for invalid GitHub URLs:

**Methods:**
- `__init__(link: str)`: Initialize with the invalid repository link

#### `GithubRepository`
Pydantic model for API request validation:

**Attributes:**
- `repository: str`: Full GitHub repository URL (required)
- `token: Optional[str]`: GitHub access token for private repositories (optional)

**Features:**
- Validates repository URL format
- Handles optional GitHub access tokens
- Ensures proper data structure for API requests

**Access the API**
   - API: http://localhost:8081
   - Documentation: http://localhost:8081/docs

## Configuration

### Environment Variables
Currently, the service uses default configurations. SSL verification is disabled for Git operations to handle corporate environments.

### Port Configuration
- Default port: `8081`
- Configurable via Docker or environment variables

## Testing

Run the test suite:
```bash
pytest tests/
```

### Test Coverage
- Invalid URL validation
- Valid URL recognition
- Multiple repository URL validation
- API connection testing
- Public repository cloning
- Private repository cloning

## Error Handling

The service handles various error scenarios:
- Invalid GitHub URLs
- Network connectivity issues
- Authentication failures
- Repository access permissions
- Filesystem errors

## Security Considerations

- SSL verification is disabled for Git operations (configurable)
- GitHub tokens are handled securely

## Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Requests**: HTTP client for tests
- **Pytest**: Testing framework

