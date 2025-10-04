# MLOps Quick Start Guide

Get your RAG-with-Gemma system running with full MLOps capabilities in minutes.

## 🚀 Quick Start (Docker - Recommended)

### 1. Start All Services

```bash
# Clone repository
git clone https://github.com/your-username/RAG-with-Gemma.git
cd RAG-with-Gemma

# Pull models (if using DVC)
dvc pull  # Optional: only if models are tracked

# Start services with Docker Compose
docker compose up -d
```

### 2. Access Services

- **RAG API**: http://localhost:8000/docs
- **MLflow**: http://localhost:5000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

### 3. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Query RAG system
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is radar calibration?",
    "top_k": 3
  }'

# View metrics
curl http://localhost:8000/metrics
```

## 📦 Local Development Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Run Locally

```bash
# Web UI
python app.py --model-path google/gemma-3-4b-it --cpu

# API Server
python run_api.py --model-path google/gemma-3-4b-it --cpu

# CLI Demo
python demo.py --model-path google/gemma-3-4b-it --interactive --cpu
```

## 🧪 Testing

### Run Unit Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html  # On Windows: start htmlcov/index.html
```

### Run Benchmarks

```bash
# Basic benchmark
python benchmark.py --model-path google/gemma-3-4b-it --cpu

# Save results
python benchmark.py --cpu --output benchmark_results.json

# Full benchmark (10 queries)
python benchmark.py --cpu --num-queries 10
```

## 🔬 Experiment Tracking with MLflow

### Run Experiment

```bash
# Start MLflow server (if not using Docker)
mlflow server --host 0.0.0.0 --port 5000

# Run experiment
python mlflow_experiment.py --model-path google/gemma-3-4b-it --cpu

# Custom experiment
python mlflow_experiment.py \
  --model-path google/gemma-3-4b-it \
  --cpu \
  --run-name "gemma-4b-cpu-optimized"
```

### Compare Experiments

```bash
# Compare all runs
python mlflow_experiment.py --compare

# View in UI
open http://localhost:5000
```

## 📊 Monitoring

### Prometheus Metrics

```bash
# View all metrics
curl http://localhost:8000/metrics

# Example metrics:
# - rag_query_total: Total queries
# - rag_query_duration_seconds: Query latency
# - rag_tokens_generated: Tokens per query
# - rag_model_memory_mb: Memory usage
```

### Grafana Dashboards

1. Open http://localhost:3000 (admin/admin)
2. Add Prometheus data source: http://prometheus:9090
3. Import dashboard from `monitoring/grafana-dashboards/`

## 🔄 Model Versioning with DVC

### Initialize DVC

```bash
# Already initialized, but to set up remote:
dvc remote add -d myremote s3://your-bucket/models  # S3
# or
dvc remote add -d myremote gs://your-bucket/models  # GCS
# or
dvc remote add -d myremote /path/to/storage  # Local
```

### Track Models

```bash
# Download and track model
huggingface-cli download google/gemma-3-4b-it --local-dir models/gemma-3-4b-it
dvc add models/gemma-3-4b-it

# Commit
git add models/gemma-3-4b-it.dvc .gitignore
git commit -m "Track Gemma 3-4B model"

# Push to remote
dvc push
```

### Pull Models

```bash
# Pull all models
dvc pull

# Pull specific model
dvc pull models/gemma-3-4b-it.dvc
```

## 🚢 Deployment

### Docker Deployment

```bash
# Build image
docker build -t rag-gemma:latest .

# Run container
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -e MODEL_PATH=google/gemma-3-4b-it \
  rag-gemma:latest
```

### Production Checklist

- [ ] Set up DVC remote storage (S3/GCS)
- [ ] Configure secrets management (.env)
- [ ] Set up Prometheus alerting rules
- [ ] Configure Grafana dashboards
- [ ] Enable authentication on APIs
- [ ] Set up log aggregation
- [ ] Configure auto-scaling (if needed)
- [ ] Set up backup strategy

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```bash
# Model configuration
MODEL_PATH=google/gemma-3-4b-it
USE_CPU=true
QUANTIZE_4BIT=false

# Document paths (pipe-delimited for multiple)
DOCUMENT_PATH=radar-calibration-doc.md

# MLflow
MLFLOW_TRACKING_URI=http://localhost:5000

# API
API_HOST=0.0.0.0
API_PORT=8000
```

### Docker Compose Override

Create `docker-compose.override.yml`:

```yaml
version: '3.8'

services:
  rag-api:
    environment:
      - MODEL_PATH=google/gemma-3-12b-it  # Use larger model
      - USE_CPU=false  # Use GPU
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## 🐛 Troubleshooting

### Issue: Container Out of Memory

```bash
# Increase Docker memory limit
# Docker Desktop -> Settings -> Resources -> Memory: 16GB

# Or use smaller model
docker compose down
# Edit docker-compose.yml: MODEL_PATH=google/gemma-3-4b-it
docker compose up -d
```

### Issue: DVC Remote Not Found

```bash
# Check remote
dvc remote list

# Add remote
dvc remote add -d myremote s3://bucket/path
```

### Issue: MLflow Not Tracking

```bash
# Check MLflow server is running
curl http://localhost:5000/health

# Set tracking URI
export MLFLOW_TRACKING_URI=http://localhost:5000
```

### Issue: Prometheus Not Scraping

```bash
# Check metrics endpoint
curl http://localhost:8000/metrics

# Check Prometheus targets
open http://localhost:9090/targets
```

## 📚 Next Steps

1. **Read Full Documentation**:
   - [MLOPS.md](MLOPS.md) - Complete MLOps guide
   - [README.md](README.md) - Project overview

2. **Customize for Your Use Case**:
   - Add your documents to `data/`
   - Update queries in benchmark scripts
   - Configure DVC for your storage

3. **Set Up CI/CD**:
   - Push to GitHub to trigger Actions
   - Configure deployment pipeline
   - Set up staging/production environments

4. **Monitor in Production**:
   - Set up Prometheus alerts
   - Create custom Grafana dashboards
   - Configure log aggregation (ELK, Splunk, etc.)

## 🤝 Getting Help

- **Issues**: https://github.com/your-username/RAG-with-Gemma/issues
- **Discussions**: https://github.com/your-username/RAG-with-Gemma/discussions
- **Documentation**: See [MLOPS.md](MLOPS.md)

---

**Happy Building! 🎉**
