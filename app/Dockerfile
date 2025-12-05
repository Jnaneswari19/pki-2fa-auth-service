# Use Python 3.10 slim
FROM python:3.10-slim

# Install cron and bash
RUN apt-get update && apt-get install -y cron bash

# Set working directory
WORKDIR /app

# Copy application code
COPY app/ /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure /data exists and is writable
RUN mkdir -p /data && chmod 777 /data

# Optional: copy seed file into container
COPY data/seed.txt /data/seed.txt

# Copy cron job file and set permissions
COPY app/cron/2fa-cron /etc/cron.d/2fa-cron
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron

# Start cron in foreground and uvicorn
CMD ["sh", "-c", "cron -f & uvicorn main:app --host 0.0.0.0 --port 8000"]
