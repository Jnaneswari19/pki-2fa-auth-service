# Base image
FROM python:3.10-slim

# Install cron and procps (for debugging)
RUN apt-get update && apt-get install -y cron procps

# Set working directory
WORKDIR /app

# Copy cron file
COPY app/cron/2fa-cron /etc/cron.d/2fa-cron

# Set permissions
RUN chmod 0644 /etc/cron.d/2fa-cron

# Ensure log file exists
RUN touch /var/log/cron.log

# Start cron in foreground
CMD cron -f
