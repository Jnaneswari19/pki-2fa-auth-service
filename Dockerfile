# Base image
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y cron bash

# Set working directory
WORKDIR /app

# Copy app code
COPY app/ /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure /data exists
RUN mkdir -p /data && chmod 777 /data

# Copy cron job
COPY app/cron/2fa-cron /etc/cron.d/2fa-cron
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron

# Copy seed files
COPY data/seed.txt /data/seed.txt
COPY data/encrypted_seed.txt /data/encrypted_seed.txt

# Run cron + FastAPI
CMD ["sh", "-c", "cron -f & uvicorn main:app --host 0.0.0.0 --port 8000"]
