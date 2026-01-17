# Use slim Debian image for faster builds
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (non-interactive)
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron gcc libffi-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and keys
COPY app /app/app
COPY scripts /app/scripts
COPY student_private.pem /app/student_private.pem
COPY student_public.pem /app/student_public.pem

# Create data directory
RUN mkdir -p /app/data

# Add cron job: heartbeat every minute
RUN echo '* * * * * echo \"$(date) heartbeat\" >> /app/data/cron.log' > /etc/cron.d/heartbeat \
 && chmod 0644 /etc/cron.d/heartbeat \
 && crontab /etc/cron.d/heartbeat

# Expose FastAPI port
EXPOSE 8000

# Start cron and FastAPI
CMD ["sh", "-c", "cron & exec uvicorn app.main:app --host 0.0.0.0 --port 8000"]
