FROM python:3.9-slim

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install nats-py and postgres adapter
RUN pip install --no-cache-dir nats-py psycopg2-binary

COPY . .

ENV PYTHONUNBUFFERED=1