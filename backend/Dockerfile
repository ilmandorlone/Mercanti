# Usa una base image di Python
FROM python:3.9-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file requirements.txt e installa le dipendenze
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install debugpy

# Copia tutto il codice del backend
COPY . /app

# Comando di avvio
CMD ["python", "run_uvicorn.py"]
