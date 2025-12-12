#!/bin/sh

# Start cron in background
service cron start

# Start FastAPI with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
