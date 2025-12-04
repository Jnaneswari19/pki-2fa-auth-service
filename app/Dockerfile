# Install cron
RUN apt-get update && apt-get install -y cron

# Copy cron job file
COPY cron/2fa-cron /etc/cron.d/2fa-cron
RUN chmod 0644 /etc/cron.d/2fa-cron \
    && crontab /etc/cron.d/2fa-cron

# Ensure logs folder exists
RUN mkdir -p /cron

# Start cron and Uvicorn
CMD cron && uvicorn main:app --host 0.0.0.0 --port 8000
