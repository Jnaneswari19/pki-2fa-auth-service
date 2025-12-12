# Stage 1: Builder
FROM python:3.9-slim AS builder

WORKDIR /app

# Install Python dependencies into user-local path
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim

WORKDIR /app

# Install cron and other utilities
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Set cron job permissions
COPY app/cron/2fa-cron /etc/cron.d/2fa-cron
RUN chmod 0644 /etc/cron.d/2fa-cron
RUN crontab /etc/cron.d/2fa-cron

# Expose FastAPI port
EXPOSE 8000

# Copy start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Run both cron and FastAPI
CMD ["/start.sh"]
