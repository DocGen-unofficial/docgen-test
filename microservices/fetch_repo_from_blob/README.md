Modulo 'Fetch repo from blob':

Recupera i blob e i container selezionati da un contaier di Azure Blob Storage e li salva in formato originale oppure convertiti in parquet.

- Cartella endpoints:
    - File api.py: Contiene gli endpoint per la gestione dei blob e dei container.

- Cartella source:
    - File container_services.py: Contiene i servizi per la gestione dei container.
    - File blob_services.py: Contiene i servizi per la gestione dei blob.
    - File schemas.py: Contiene le classi pydantic per la validazione dei dati e maggiore ordine nel codice.

- Cartella tests:
    - File test_fetch_repo_from_blob.py: Contiene i test per gli endpoint e i servizi.

- Cartella utilities:
    - File retry.py: Contiene le funzioni per la gestione dei retry in caso di errori durante le operazioni sui blob e container.

- Dockerfile:
    - File Dockerfile: Contiene le istruzioni per la creazione dell'immagine Docker del servizio.

- main.py:
    - File main.py: Contiene il codice per l'avvio del servizio FastAPI.

- requirements.txt:
    - File requirements.txt: Contiene le dipendenze del progetto.

        