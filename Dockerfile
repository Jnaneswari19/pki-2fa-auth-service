# STEP 1: Use Python base image
FROM python:3.10-slim

# STEP 2: Install cron
RUN apt-get update && apt-get install -y cron

# STEP 3: Set working directory
WORKDIR /app

# STEP 4: Copy project files
COPY . /app

# STEP 5: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# STEP 6: Copy cron job file into system cron.d
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# STEP 7: Give execution permission
RUN chmod 0644 /etc/cron.d/2fa-cron

# STEP 8: Apply cron job
RUN crontab /etc/cron.d/2fa-cron

# STEP 9: Create folder to store last_code.txt
RUN mkdir -p /cron

# STEP 10: Start cron + start API
CMD ["sh", "-c", "cron -f & uvicorn main:app --host 0.0.0.0 --port 8000"]

