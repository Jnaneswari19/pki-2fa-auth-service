# Stage 1: Builder
FROM python:3.9-slim AS builder

WORKDIR /app

# Install dependencies into a user-local path
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local

# Update PATH so Python can find installed packages
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

