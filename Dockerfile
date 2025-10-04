# Multi-stage build for RAG with Gemma
FROM python:3.11-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for models and data
RUN mkdir -p /app/models /app/data /app/logs

# Expose ports for API and MLflow
EXPOSE 8000 5000

# Default command (can be overridden in docker-compose)
CMD ["python", "run_api.py", "--model-path", "google/gemma-3-4b-it", "--cpu", "--host", "0.0.0.0"]
