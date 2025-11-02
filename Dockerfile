FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD sh -c "\
    until nc -z $DB_HOST $DB_PORT; do echo 'Waiting for database...'; sleep 2; done && \
    python -m scripts.create_db && \
    python -m scripts.seed_data && \
    uvicorn main:app --host 0.0.0.0 --port 5000"
