# Orchestrator Microservice

A Python microservice to orchestrate the end-to-end workflow of downloading, uploading, and transforming GitHub repositories via REST calls to specialized microservices.

## Overview

This microservice acts as an orchestrator, coordinating the interaction between several microservices:
- **GitHub repository download**
- **Upload to Azure Blob Storage**
- **Transformation to Parquet format**

The orchestrator sends HTTP requests to the involved services, managing the data flow and the sequence of operations.

## Architecture & Workflow

### System Architecture
```
┌────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Client   │──▶│ Orchestrator │──▶│ RepoDownloader│──▶│Uploader/Blob │
└────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                                              │
                                              ▼
                                    ┌────────────────────┐
                                    │ Transformer/Parquet│
                                    └────────────────────┘
```

### Workflow
1. **Download**: POST to `/v1/download_repository` of the repo_downloader microservice
2. **Upload**: POST to `/v2/repo/upload` of the uploader microservice, passing the local repo path
3. **Transformation**: POST to `/v3/transform-container-to-parquet` for Parquet conversion

Each step receives the response from the previous one and uses it as input for the next.

## Main Components

- **main.py**: Entry point, manages the sequence of REST calls and orchestration logic
- **source/apicalls.py**: Support functions for HTTP calls and response handling

## Microservice Structure

```
orchestrator/
├── README.md          # Documentation
├── main.py            # Entry point, sequential workflow
├── Dockerfile         # Containerization
├── requirements.txt   # Dependencies
├── source/
│   └── apicalls.py    # API call functions
└── tests/
    └── test_workflow.py # Pytest-based tests
```

## Example Workflow (main.py)

```python
if __name__ == "__main__":
    response = requests.post("http://localhost:5001/v1/download_repository", json=json_request_body)
    print("Step 1 complete")
    response = requests.post("http://localhost:5002/v2/repo/upload", params={"repo_path": response.json()["path"]})
    print(response.json())
    container = response.json()["container_name"]
    print("Step 2 complete")
    response = requests.post("http://localhost:5003/v3/transform-container-to-parquet", json={'container_name': container, 'single_parquet': True})
    print(response.json()["message"])
```

## Containerization & Deployment

### Dockerfile
- **Base Image**: python:3.11-slim
- **WORKDIR**: /app
- **Dependencies**: installed from requirements.txt
- **Expose**: 8089 (configurable)
- **CMD**: Automatically runs `main.py`

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8089
CMD ["python", "main.py"]
```

## Dependencies

All dependencies are listed in `requirements.txt`:

```
requests
pytest
```

- **requests**: HTTP client for REST calls
- **pytest**: Testing framework

Install them with:
```bash
pip install -r requirements.txt
```

## Testing

Automated tests are provided in the `tests/` folder and use `pytest`.

- `test_workflow.py` covers:
  - **API call logic in `apicalls.py`**: All HTTP requests are mocked to simulate both successful and failed responses, ensuring robust error handling and correct data extraction.
  - **Main workflow in `main.py`**: The full orchestration sequence is tested con mocking delle chiamate HTTP verso i servizi downstream, verificando che ogni step venga eseguito e che il flusso sia quello atteso.

### Test details

- `test_get_repo_status`: Verifica che la funzione di status del repository ritorni il codice corretto (mock di `requests.get`).
- `test_get_repo_url_success`: Simula una risposta positiva dal servizio di download e verifica che il percorso venga estratto correttamente.
- `test_get_repo_url_failure`: Simula una risposta fallita e verifica che venga gestito il caso di errore.
- `test_main_workflow`: Esegue l'intero workflow orchestrato, mockando tutte le chiamate HTTP e verificando che ogni step sia chiamato nell'ordine corretto.

Tutte le funzioni di mock sono definite all'interno del file di test e vengono applicate tramite `monkeypatch` di pytest, garantendo isolamento e ripetibilità dei test.

To run the tests:
```bash
pytest 
```
or

```bash
pytest tests/
```
