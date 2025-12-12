# Copy cron job definition
COPY app/cron/test-cron /etc/cron.d/test-cron

# Set correct permissions
RUN chmod 0644 /etc/cron.d/test-cron

# Register cron job
RUN crontab /etc/cron.d/test-cron

# Ensure log file exists
RUN touch /tmp/test.log

# Keep cron alive in foreground
CMD cron -f
