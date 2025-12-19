FROM python:3.11-alpine

WORKDIR /app

# Install cron (dcron) and build tools
RUN apk add --no-cache gcc musl-dev libffi-dev dcron

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Add cron job: heartbeat every minute
RUN echo '* * * * * echo "$(date) heartbeat" >> /app/data/cron.log' > /etc/crontabs/root

# Expose FastAPI port
EXPOSE 8000

# Start cron and FastAPI together
CMD crond && uvicorn app.main:app --host 0.0.0.0 --port 8000
