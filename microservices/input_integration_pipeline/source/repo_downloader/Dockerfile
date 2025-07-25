FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia il certificato custom nel container
#COPY custom-ca-bundle.pem /usr/local/share/ca-certificates/custom-ca-bundle.crt

# Aggiornamento i certificati CA (per Debian/Ubuntu)
#RUN update-ca-certificates

# Configurazione git per usare il bundle aggiornato
#RUN git config --global http.sslCAInfo /etc/ssl/certs/ca-certificates.crt

## Disabilitazione SSL
RUN git config --global http.sslVerify false

COPY . .

EXPOSE 8081

CMD ["python", "main.py"]