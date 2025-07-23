# Microservizio Upload Repo on Blob

Microservizio basato su FastAPI per caricare una repository locale (ad esempio clonata da GitHub) su Azure Blob Storage. Ideale per pipeline di orchestrazione e scenari di automazione.

## Panoramica

Questo microservizio espone endpoint REST API per caricare il contenuto di una repository locale su un container di Azure Blob Storage. Include la validazione della connessione, la creazione automatica del container e la normalizzazione del nome per rispettare i requisiti di Azure.

## Architettura & Workflow

### Architettura del Sistema
```
┌────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Client   │───▶│  FastAPI Server  │───▶│ Azure Blob Storage │
│ (HTTP Req) │    │  (Porta 8082)    │    │ (Container/Blobs)   │
└────────────┘    └──────────────────┘    └─────────────────────┘
                         │
                         ▼
                  ┌───────────────┐
                  │   Risposta    │
                  │    (JSON)     │
                  └───────────────┘
```

### Flusso della Richiesta
1. **Richiesta Client**: HTTP POST a `/v2/repo/upload`
2. **Validazione API**: Modello Pydantic valida i dati della richiesta
3. **Normalizzazione Nome Container**: Assicura nomi compatibili con i requisiti Azure
4. **Verifica Connessione**: Controlla la connessione ad Azure Blob Storage
5. **Creazione Container**: Crea il container se non esiste
6. **Upload File**: Carica ricorsivamente tutti i file della repository locale
7. **Risposta**: Restituisce stato di successo/errore e dettagli

### Architettura di Deploy
- **Container**: Docker container con Python 3.11-slim
- **Porta**: 8082 (configurabile)
- **CORS**: Abilitato per richieste cross-origin

### Containerizzazione & Orchestrazione

#### Dockerfile
Il Dockerfile permette il deploy containerizzato e l’orchestrazione:

**Caratteristiche principali:**
- **Base Image**: Python 3.11-slim per un container leggero
- **Gestione Dipendenze**: Installa le dipendenze Python da `requirements.txt`
- **Esposizione Porta**: Espone la porta 8082 per l’accesso API

## Funzionalità

- **Upload Repository**: Carica tutti i file di una repository locale su Azure Blob Storage
- **Creazione Automatica Container**: Crea il container se non esiste
- **Verifica Connessione**: Endpoint per testare la connessione ad Azure
- **Sanitizzazione Nome Container**: Assicura nomi compatibili con Azure
- **Supporto Docker**: Pronto per il deploy containerizzato
- **Upload Parallelo**: Ottimizzazione delle performance di upload

## Endpoint API

### Verifica Connessione / Health Check
```http
GET /v2/repo/check_connection
```
Restituisce lo stato della connessione ad Azure Blob Storage.

**Risposta:**
```json
{
  "message": "Connessione avvenuta con successo"
}
```

### Upload Repository
```http
POST /v2/repo/upload?repo_path=/percorso/alla/repository
```

**Parametro Query:**
- `repo_path`: Percorso locale della repository da caricare

**Risposta (Successo):**
```json
{
  "message": "Repository caricata con successo.",
  "container": "nome-container",
  "files_uploaded": 123
}
```

**Risposta (Errore):**
```json
{
  "message": "Caricamento repository fallito.",
  "error": "Connection string non valida o percorso non trovato"
}
```

## Componenti Principali

- **`main.py`**: Entry point FastAPI con middleware CORS
- **`src/endpoints/endpoint_uploader.py`**: Definizione delle rotte API per upload e verifica connessione
- **`src/services/uploader.py`**: Logica principale di upload su Azure Blob Storage
- **`src/services/blob_manager.py`**: Gestione connessione e container Azure
- **`src/utils/helpers.py`**: Funzioni di utilità (es. sanitizzazione nomi)
- **`src/config/settings.py`**: Gestione configurazione e variabili ambiente

## Struttura del Microservizio

```
upload_repo_on_blob/
├── main.py                     # Entry point FastAPI
├── requirements.txt            # Dipendenze Python
├── Dockerfile                  # Configurazione container
├── README.md                   # Documentazione progetto
└── src/
    ├── config/
    │   └── settings.py         # Gestione configurazione
    ├── endpoints/
    │   └── endpoint_uploader.py # Definizione rotte API
    ├── services/
    │   ├── blob_manager.py     # Gestione Azure Blob
    │   └── uploader.py         # Logica upload
    └── utils/
        └── helpers.py          # Funzioni utilità
```

### Classi Principali

#### `Uploader`
Gestisce l’upload dei file della repository su Azure Blob Storage.

**Metodi:**
- `__init__(repo_path: str, container_name: str)`: Inizializza con percorso locale e nome container
- `upload_all_files() -> int`: Carica tutti i file e restituisce il conteggio

#### `BlobManager`
Gestisce la connessione e le operazioni sui container Azure Blob Storage.

**Metodi:**
- `check_connection() -> bool`: Verifica la connessione ad Azure
- `create_container_if_not_exists(name: str)`: Crea il container se non esiste

#### `sanitize_container_name`
Funzione di utilità per rendere i nomi dei container compatibili con Azure.

## Accesso all’API

- API: http://localhost:8082
- Documentazione: http://localhost:8082/docs

## Configurazione

### Variabili d’Ambiente

- `AZURE_STORAGE_CONNECTION_STRING`: Stringa di connessione ad Azure Blob Storage (obbligatoria)

### Configurazione Porta

- Porta di default: `8082`
- Configurabile tramite Docker o variabili d’ambiente

## Testing

Puoi aggiungere test per:
- Validazione connessione
- Logica di upload
- Sanitizzazione nomi container

## Gestione Errori

Gestisce errori come:
- Stringhe di connessione non valide
- Percorsi repository mancanti o errati
- Permessi Azure insufficienti
- Errori filesystem

## Sicurezza

- Le stringhe di connessione devono essere gestite in modo sicuro (es. variabili d’ambiente)