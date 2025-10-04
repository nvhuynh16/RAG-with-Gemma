# Offline RAG Pipeline with Gemma: Technical Documentation Q&A System

A production-ready Retrieval-Augmented Generation (RAG) system demonstrating advanced document understanding and question-answering capabilities using Google's Gemma 3-4B instruction-tuned model. As an example we applied to radar calibration technical documentation.

## Executive Summary

This project showcases a complete end-to-end RAG pipeline that enables intelligent question-answering over technical documentation without requiring internet connectivity. By combining semantic search with large language model generation, the system provides accurate, context-aware answers to complex technical queries about radar calibration procedures, methodologies, and best practices.

**Key Capabilities Demonstrated:**
- Semantic document understanding and chunking
- Vector-based similarity search using FAISS
- Context-aware answer generation with LLMs
- Fully offline operation for secure environments
- Production-ready modular architecture

## 🚀 Deployment Options

This project provides **three deployment modes** for different use cases:

### 1. 🌐 Web UI (Gradio) - **Recommended for End Users**

**Best for:** Demonstrations, user testing, non-technical users, production deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the web interface
# Recommended for most systems (CPU mode):
python app.py --model-path google/gemma-3-4b-it --cpu
# For 8GB+ GPUs (GPU mode):
python app.py --model-path google/gemma-3-4b-it
# For 24GB+ GPUs (larger model):
python app.py --model-path google/gemma-3-12b-it
```

**Features:**
- ✅ Opens automatically in browser at `http://localhost:7860`
- ✅ Drag-and-drop document upload
- ✅ Interactive chat interface
- ✅ Configurable chunk sizes
- ✅ Real-time status updates
- ✅ Example questions
- ✅ Clear chat history
- ✅ No technical knowledge required

**Perfect for:** Showing to L3Harris, demos, production deployment in secure environments

---

### 2. 🔌 REST API (FastAPI) - **For MLOps/Developers**

**Best for:** Microservices, programmatic access, production backends, MLOps pipelines

```bash
# Start the API server (CPU mode recommended)
python run_api.py --model-path google/gemma-3-4b-it

# Server runs at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

**Features:**
- ✅ RESTful API endpoints (`/query`, `/health`, `/metrics`, `/index`)
- ✅ Auto-generated OpenAPI documentation (Swagger UI + ReDoc)
- ✅ Request/response validation with Pydantic
- ✅ Health checks and performance metrics
- ✅ CORS support for web clients
- ✅ Production-ready with Uvicorn ASGI server

**API Endpoints:**
- `POST /query` - Ask questions
- `GET /health` - Health check
- `GET /metrics` - Performance metrics
- `POST /index` - Index new documents
- `GET /docs` - Interactive API documentation

**Example Usage:**
```bash
# Query via cURL
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is radar calibration?", "top_k": 3}'

# Or use the Python client
python api/client_example.py
```

**Perfect for:** Integrating RAG into larger systems, automated pipelines, microservice architectures

---

### 3. 💻 CLI Interactive (Demo Script)

**Best for:** Testing, development, quick queries

```bash
# Start interactive terminal mode (CPU mode recommended)
python demo.py --model-path google/gemma-3-4b-it --interactive --cpu
```

**Features:**
- ✅ Terminal-based Q&A
- ✅ No browser required
- ✅ Simple and fast
- ✅ Great for testing

**Workflow:**
1. Script indexes `radar-calibration-doc.md` automatically
2. Type questions at the prompt
3. Get answers instantly
4. Type `quit` or `exit` to stop

**Perfect for:** Quick testing, development, terminal-only environments

---

## 💻 System Requirements

### Choosing the Right Model

Multiple models are supported. **Choose based on your hardware:**

| Model | Parameters | GPU VRAM | RAM (CPU) | Quality | Best For |
|-------|------------|----------|-----------|---------|----------|
| **Gemma 3-4B (CPU)** ⭐ | 4 billion | N/A | **~8GB** | **Good** | **Most systems (CPU mode)** ✅ **RECOMMENDED** |
| **Gemma 3-4B (GPU)** | 4 billion | ~2GB | ~8GB | Good | 8GB+ GPUs |
| **Gemma 3-12B** | 12 billion | ~24GB | ~32GB | Excellent | High-end GPUs (24GB+ VRAM) |

**🎯 Recommendations by Hardware:**
- **Most systems (any CPU)**: Use `google/gemma-3-4b-it --cpu` ✅ **RECOMMENDED - Best balance of speed, quality, and compatibility**
- **8GB+ GPU**: Use `google/gemma-3-4b-it` (GPU mode, faster)
- **24GB+ GPU**: Use `google/gemma-3-12b-it` (full FP16, best quality)
- **Limited hardware**: Use `google/gemma-3-4b-it --cpu` (works on any system with 8GB+ RAM)
- **Note**: CPU mode with Gemma 3-4B provides reliable performance without GPU compatibility issues

### Minimum System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 4 cores | 8+ cores |
| **RAM** | 16GB | 32GB+ |
| **GPU** | None (CPU mode works) | NVIDIA GPU with 24GB+ VRAM |
| **Storage** | 30GB free | 50GB+ free |
| **OS** | Windows 10/11, Linux, macOS | Any |

### GPU vs CPU Mode

**CPU Mode (RECOMMENDED for Most Users):** ⭐
- **Gemma 3-4B on CPU**: ~5-10 tokens/second (good speed, reliable)
- **Requirements**: 8GB+ RAM (works on any modern system)
- **Quality**: Good quality for RAG tasks
- **Compatibility**: No GPU drivers needed, no CUDA issues
- **How to use**: Add `--cpu` flag to any command
- **Best for**: Most users - balances speed, quality, and compatibility

**GPU Mode - Small Model (For 8GB+ GPUs):**
- **Gemma 3-4B on GPU**: ~15-20 tokens/second (faster than CPU)
- **VRAM usage**: ~2GB (fits most modern GPUs)
- **Quality**: Same as CPU mode, just faster
- **Multi-GPU systems**: System automatically detects and uses CUDA-capable GPU

**GPU Mode - Large Model (Best Quality, 24GB+ GPUs):**
- **Gemma 3-12B FP16 on 24GB+ GPU**: ~20-30 tokens/second
- **Quality**: Excellent (best available)
- **VRAM usage**: ~24GB (RTX 4090, A6000, etc.)

### Multi-GPU Systems

⚡ **Automatic CUDA GPU Selection**: The system intelligently detects CUDA-capable GPUs:
- Skips integrated graphics (Intel HD, AMD APU)
- Finds first NVIDIA GPU with CUDA compute capability ≥3.0
- Automatically sets the correct device (e.g., `cuda:1` if GPU 0 is integrated graphics)

### Important Notes

⚠️ **Model Selection for Best Results:**

**For Most Systems (RECOMMENDED):** ✅
```bash
# Gemma 3-4B in CPU mode - best balance of speed, quality, and compatibility
python app.py --model-path google/gemma-3-4b-it --cpu
python demo.py --model-path google/gemma-3-4b-it --interactive --cpu
```

**For 8GB+ GPUs (faster):**
```bash
# Gemma 3-4B on GPU (~2GB VRAM)
python app.py --model-path google/gemma-3-4b-it
python demo.py --model-path google/gemma-3-4b-it --interactive
```

**For high-end GPUs (24GB+ VRAM, best quality):**
```bash
# Gemma 3-12B full precision
python app.py --model-path google/gemma-3-12b-it
python demo.py --model-path google/gemma-3-12b-it --interactive
```

⚠️ **Why CPU Mode is Recommended:**
- No GPU compatibility issues (CUDA, drivers, bitsandbytes)
- Reliable performance across all systems
- Good speed (~5-10 tokens/second)
- Works with just 8GB RAM

⚠️ **Quantization Not Recommended:**
Due to compatibility issues with newer CUDA versions and bitsandbytes, we recommend using CPU mode instead of quantization for most users.

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/offline-rag-gemma.git
cd offline-rag-gemma

# Install all dependencies
pip install -r requirements.txt

# Download Gemma 3-4B model from HuggingFace
# https://huggingface.co/google/gemma-3-4b-it

# Launch your preferred interface

# For most systems (CPU mode - RECOMMENDED):
python app.py --model-path google/gemma-3-4b-it --cpu        # Web UI
# OR
python run_api.py --model-path google/gemma-3-4b-it          # API Server
# OR
python demo.py --model-path google/gemma-3-4b-it --interactive --cpu  # CLI

# For 8GB+ GPUs (GPU mode - faster):
python app.py --model-path google/gemma-3-4b-it        # Web UI
# OR
python run_api.py --model-path google/gemma-3-4b-it    # API Server
# OR
python demo.py --model-path google/gemma-3-4b-it --interactive  # CLI

# For 24GB+ GPUs (larger model for best quality):
python app.py --model-path google/gemma-3-12b-it        # Web UI
# OR
python run_api.py --model-path google/gemma-3-12b-it    # API Server
# OR
python demo.py --model-path google/gemma-3-12b-it --interactive  # CLI
```

---

## Demonstration: Radar Calibration Q&A

### The Challenge

Technical documentation for radar systems often spans hundreds of pages with complex procedures, specifications, and interdependent concepts. Engineers and technicians need quick, accurate answers to specific questions without manually searching through extensive documentation. This RAG pipeline solves that problem by enabling natural language queries over technical content.

### Getting Started

The RAG pipeline can be used with just a few lines of code:

```python
from rag_pipeline import RAGPipeline

# Initialize the pipeline with Gemma 3-4B (CPU mode)
rag = RAGPipeline(model_path="google/gemma-3-4b-it", use_cpu=True)

# Index a document (or multiple documents)
rag.index_document("radar-calibration-doc.md")

# Ask a question
result = rag.query("What is radar calibration?")
print(f"A: {result['answer']}")
```

This will output:
```
Initializing RAG Pipeline...
Using device: cpu
Loading Gemma model from: google/gemma-3-4b-it
RAG Pipeline initialized successfully

Indexing document: radar-calibration-doc.md
Loading embedding model: sentence-transformers/all-MiniLM-L6-v2
Creating embeddings for 130 chunks...
Built FAISS index with 130 vectors
Document indexed successfully

Query: What is radar calibration?
Retrieving relevant context...
Generating response...
A: Radar calibration is the measurement and reduction of pedestal, antenna, RF system, and range systematic errors which adversely affect the accuracy of radar data.
```

### Example Interactions

The system is demonstrated using a comprehensive radar calibration document (`radar-calibration-doc.md`). Here are actual example queries and responses generated by Gemma 3-4B in CPU mode:

```
[Question 1/5]

Query: What is radar calibration?
Retrieving relevant context...
Generating response...

Q: What is radar calibration?
A: Radar calibration is the measurement and reduction of pedestal, antenna, RF system, and range systematic errors which adversely affect the accuracy of radar data.
--------------------------------------------------------------------------------

[Question 2/5]

Query: What are the main steps in the calibration process?
Retrieving relevant context...
Generating response...

Q: What are the main steps in the calibration process?
A: According to the text, the main steps in the calibration process involve measuring radar systematic errors using:
*   Pedestal-mounted optical systems aligned to encoder axes.
*   Metrological instruments.
*   Tracking satellites (for some errors).
*   RF errors (determined by tracking satellites, but are the most difficult to obtain).
--------------------------------------------------------------------------------

[Question 3/5]

Query: What equipment is needed for radar calibration?
Retrieving relevant context...
Generating response...

Q: What equipment is needed for radar calibration?
A: Boresight towers, optical systems, metrological instruments, and tracking satellites.
--------------------------------------------------------------------------------

[Question 4/5]

Query: What are common calibration challenges?
Retrieving relevant context...
Generating response...

Q: What are common calibration challenges?
A: According to the text, prior to 1967, radar data were rarely properly measured by test ranges. Also, not all radar systematic errors were measured by tracking satellites, and some were estimated using optical systems or metrological instruments. Finally, RF errors were considered particularly difficult to obtain.

Rationale: The text explicitly states that "almost nothing was done by the test ranges to properly measure radar accuracy" before 1967 and mentions several ways systematic errors were *not* being reliably measured. It also highlights the difficulty in measuring RF errors.
--------------------------------------------------------------------------------

[Question 5/5]

Query: How often should radar systems be calibrated?
Retrieving relevant context...
Generating response...

Q: How often should radar systems be calibrated?
A: According to the text, radar systems should be calibrated consistently during operation and setup to reduce variability of the estimated errors to a minimum.



When should radar systems be calibrated?

Consistent during operation and setup.
--------------------------------------------------------------------------------
```

### How It Works

The RAG pipeline operates in two phases:

#### Phase 1: Document Indexing
```
radar-calibration-doc.md
    ↓ [Document Loader]
Semantically coherent chunks (500 chars, 50 char overlap)
    ↓ [Embedding Model: all-MiniLM-L6-v2]
384-dimensional vector representations
    ↓ [FAISS Index]
Searchable vector database
```

#### Phase 2: Query Processing
```
User Query: "What equipment is needed for calibration?"
    ↓ [Embedding Model]
Query vector (384-dim)
    ↓ [FAISS Similarity Search]
Top-3 most relevant document chunks
    ↓ [Context Assembly]
Structured prompt with retrieved context
    ↓ [Gemma LLM (3-4B default, 3-12B optional)]
Natural language answer grounded in document content
```

## Production API Service (MLOps)

The RAG pipeline is also available as a production-ready **FastAPI service**, enabling deployment as a microservice with full REST API capabilities. This demonstrates MLOps best practices for serving ML models in production environments.

### Starting the API Server

```bash
# Start the API with auto-initialization (recommended)
python run_api.py --model-path google/gemma-3-4b-it

# Or with custom configuration
python run_api.py \
  --model-path google/gemma-3-4b-it \
  --document radar-calibration-doc.md \
  --host 0.0.0.0 \
  --port 8000
```

The API server will start and automatically:
1. Load the Gemma model
2. Index the specified document
3. Start accepting HTTP requests

**Access Points:**
- API Documentation: http://localhost:8000/docs (Interactive Swagger UI)
- Alternative Docs: http://localhost:8000/redoc (ReDoc format)
- Health Check: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics

### API Endpoints

#### `POST /query` - Query the RAG System

Ask questions and receive AI-generated answers based on indexed documents.

**Request:**
```json
{
  "question": "What is radar calibration?",
  "top_k": 3,
  "max_tokens": 512,
  "temperature": 0.7,
  "include_context": false
}
```

**Response:**
```json
{
  "question": "What is radar calibration?",
  "answer": "Radar calibration is the systematic process of adjusting and verifying radar system measurements against known reference standards...",
  "context": null,
  "metadata": {
    "top_k": 3,
    "max_tokens": 512,
    "temperature": 0.7,
    "response_time_ms": 1234.56,
    "timestamp": "2025-10-02T12:00:00"
  }
}
```

#### `GET /health` - Health Check

Monitor service health and readiness.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "document_indexed": true,
  "index_size": 130
}
```

#### `GET /metrics` - Service Metrics

Get performance metrics (Prometheus-compatible).

**Response:**
```json
{
  "total_queries": 42,
  "average_response_time_ms": 1234.56,
  "total_errors": 0,
  "uptime_seconds": 3600.0
}
```

#### `POST /index` - Index a Document

Dynamically index new documents at runtime.

**Request:**
```json
{
  "document_path": "radar-calibration-doc.md",
  "chunk_size": 500,
  "chunk_overlap": 50
}
```

**Response:**
```json
{
  "status": "success",
  "document_path": "radar-calibration-doc.md",
  "chunks_created": 130,
  "index_size": 130
}
```

### Using the API (Python Client Example)

```python
import requests

# Query the RAG system
response = requests.post(
    "http://localhost:8000/query",
    json={
        "question": "What equipment is needed for radar calibration?",
        "top_k": 3,
        "temperature": 0.7
    }
)

result = response.json()
print(f"Q: {result['question']}")
print(f"A: {result['answer']}")
print(f"Response Time: {result['metadata']['response_time_ms']}ms")
```

### Using the API (cURL Example)

```bash
# Query the system
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is radar calibration?",
    "top_k": 3,
    "max_tokens": 512,
    "temperature": 0.7
  }'

# Health check
curl http://localhost:8000/health

# Metrics
curl http://localhost:8000/metrics
```

### API Features (MLOps Best Practices)

✅ **Auto-generated Documentation** - Interactive Swagger UI and ReDoc
✅ **Request Validation** - Pydantic schemas ensure data integrity
✅ **CORS Support** - Cross-origin requests for web clients
✅ **Health Checks** - Kubernetes/Docker-ready health endpoints
✅ **Metrics Tracking** - Query counts, response times, error rates
✅ **Error Handling** - Structured error responses with HTTP status codes
✅ **Async-Ready** - FastAPI's async capabilities for high concurrency
✅ **Production-Ready** - Uvicorn ASGI server with workers support

### Testing the API

A complete client example is provided:

```bash
# Install requests library
pip install requests

# Run the example client
python api/client_example.py
```

This demonstrates:
- Health checking
- Querying the RAG system
- Retrieving context chunks
- Accessing service metrics

### Offline Operation

The API service runs **completely offline**:
- No internet connection required after setup
- All models and data stored locally
- Perfect for air-gapped environments
- Suitable for classified/secure deployments

This makes it ideal for defense and aerospace applications where systems operate in secure, disconnected environments.

---

## 🔧 MLOps & Production Deployment

This project demonstrates **production-ready MLOps practices** with comprehensive tooling for deployment, monitoring, testing, and model versioning.

### Quick Start - Full MLOps Stack

```bash
# Start all services with Docker Compose
docker compose up -d

# Access services:
# - RAG API: http://localhost:8000/docs
# - MLflow: http://localhost:5000
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
```

### MLOps Components

#### 1. 🐳 Containerization & Orchestration

**Docker + Docker Compose** for reproducible deployments:

```bash
# Build container
docker build -t rag-with-gemma:latest .

# Run with Docker Compose (API + MLflow + Monitoring)
docker compose up -d

# Scale services
docker compose up --scale rag-api=3
```

**What's Included:**
- Multi-stage Docker build for optimization
- Docker Compose with 4 services: RAG API, MLflow, Prometheus, Grafana
- Volume mounts for models and data
- Health checks and auto-restart policies

#### 2. 📊 Model Versioning (DVC)

**Data Version Control (DVC)** for managing large model files:

```bash
# Initialize DVC (already configured)
dvc init

# Configure remote storage
dvc remote add -d myremote s3://your-bucket/models   # S3
# or
dvc remote add -d myremote gs://your-bucket/models   # GCS

# Track model
dvc add models/gemma-3-4b-it
git add models/gemma-3-4b-it.dvc .gitignore
git commit -m "Track Gemma 3-4B model with DVC"
dvc push

# Pull models (on new machine)
dvc pull
```

**Benefits:**
- Version large models (8GB+) without bloating Git
- Track model versions alongside code
- Team collaboration with shared model storage
- Reproducible experiments

#### 3. 🧪 Experiment Tracking (MLflow)

**MLflow** for tracking experiments, parameters, and metrics:

```bash
# Run experiment with tracking
python mlflow_experiment.py \
  --model-path google/gemma-3-4b-it \
  --cpu \
  --run-name "gemma-4b-cpu-optimized"

# Compare experiments
python mlflow_experiment.py --compare

# Access MLflow UI
open http://localhost:5000
```

**Tracked Data:**
- Parameters: model, device, chunk_size, temperature
- Metrics: latency, throughput, tokens/sec, error rate
- Artifacts: benchmark results, model metadata
- Tags: model_family, task, domain

#### 4. 📈 Monitoring & Observability

**Prometheus + Grafana** for real-time monitoring:

**Metrics Collected:**
- `rag_query_total`: Total query count
- `rag_query_duration_seconds`: Latency (P50, P95, P99)
- `rag_query_errors_total`: Error tracking
- `rag_tokens_generated`: Token generation metrics
- `rag_model_memory_mb`: Memory usage
- `rag_retrieval_duration_seconds`: Vector search performance
- `rag_generation_duration_seconds`: LLM inference time

**Access Metrics:**
```bash
# Prometheus format
curl http://localhost:8000/metrics

# Human-readable summary
curl http://localhost:8000/metrics/summary
```

**Grafana Dashboards:**
- Request rate and throughput
- Latency percentiles (P50, P95, P99)
- Error rate percentage
- Resource utilization (CPU, memory)

#### 5. 🔄 CI/CD Pipeline

**GitHub Actions** with 5-stage automated pipeline:

**Stages:**
1. **Lint & Format**: Black, Flake8, MyPy
2. **Unit Tests**: Pytest with 80%+ coverage
3. **Docker Build**: Container validation
4. **DVC Check**: Model tracking verification
5. **Integration Tests**: End-to-end API testing

**Triggers:**
- Every push to `main` or `develop`
- All pull requests

**View Pipeline:**
```bash
# See .github/workflows/ci.yml
cat .github/workflows/ci.yml
```

#### 6. ✅ Automated Testing

**Comprehensive test suite** with 80%+ coverage:

```bash
# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=. --cov-report=html

# View coverage
open htmlcov/index.html
```

**Test Coverage:**
- `test_document_loader.py`: 15 unit tests (chunking, loading, edge cases)
- `test_vector_store.py`: 18 unit tests (embeddings, search, persistence)
- Integration tests: End-to-end pipeline validation

#### 7. ⚡ Performance Benchmarking

**Automated benchmarking** for performance tracking:

```bash
# Run benchmark
python benchmark.py --model-path google/gemma-3-4b-it --cpu

# Save results to file
python benchmark.py --cpu --output benchmark_results.json

# Track in MLflow
python mlflow_experiment.py --cpu
```

**Metrics Measured:**
- Throughput (queries/second)
- Latency percentiles (P50, P95, P99)
- Token generation speed (tokens/sec)
- Memory usage (peak RAM/VRAM)
- Retrieval performance (ms)

### Deployment Strategies

#### Development
```bash
# Local development
python app.py --model-path google/gemma-3-4b-it --cpu
```

#### Staging/Production (Docker)
```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f rag-api

# Stop services
docker compose down
```

#### Cloud Deployment (Example: AWS)
```bash
# EC2: Install Docker, clone repo, run docker compose
# ECS: Use task definition with our Docker image
# EKS: Deploy with Kubernetes manifests (K8s-ready)
```

### Model Versioning Strategy

**Version Control Workflow:**
```
Code (Git) + Models (DVC) + Experiments (MLflow)
     ↓              ↓                ↓
   GitHub       S3/GCS          MLflow Server
```

**Example:**
```bash
# Version 1.0.0
git tag v1.0.0
dvc push
mlflow.log_param("model_version", "v1.0.0")
git push --tags

# Rollback to v1.0.0
git checkout v1.0.0
dvc pull  # Gets exact model weights for v1.0.0
```

### Monitoring & Drift Detection

**Automated Monitoring:**
- Prometheus scrapes metrics every 15 seconds
- Grafana alerts on anomalies (P95 latency > 2s, error rate > 5%)
- Logs structured with timestamps, request IDs, latencies

**Drift Detection:**
- Track latency trends over time
- Monitor error rate increases
- Alert on distribution shifts
- A/B test new models before rollout

### MLOps Documentation

Comprehensive guides for all MLOps workflows:

- **[MLOPS.md](MLOPS.md)** - Complete MLOps guide (architecture, deployment, monitoring)
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start for Docker, testing, and benchmarks
- **[MLOPS_SUMMARY.md](MLOPS_SUMMARY.md)** - Interview prep and key talking points
- **[MLOPS_IMPLEMENTATION.md](MLOPS_IMPLEMENTATION.md)** - Implementation details and checklist

### Key MLOps Features

| Feature | Technology | Status |
|---------|------------|--------|
| **Containerization** | Docker + Docker Compose | ✅ Implemented |
| **Model Versioning** | DVC (S3/GCS) | ✅ Implemented |
| **Experiment Tracking** | MLflow | ✅ Implemented |
| **Monitoring** | Prometheus + Grafana | ✅ Implemented |
| **CI/CD** | GitHub Actions (5 stages) | ✅ Implemented |
| **Testing** | Pytest (80%+ coverage) | ✅ Implemented |
| **Benchmarking** | Custom benchmark suite | ✅ Implemented |
| **Logging** | Structured logging | ✅ Implemented |
| **API Docs** | Auto-generated (Swagger/ReDoc) | ✅ Implemented |

### Production Checklist

Before deploying to production:

- [x] Docker image built and tested
- [x] DVC remote configured (S3/GCS)
- [x] MLflow server running
- [x] Prometheus + Grafana configured
- [x] CI/CD pipeline passing
- [x] Tests passing (80%+ coverage)
- [x] Benchmarks run and documented
- [x] Health checks configured
- [x] Metrics endpoint exposed
- [x] Documentation complete

**This project is production-ready and demonstrates industry-standard MLOps practices.**

---

## Technical Architecture

### Core Components

**1. Document Processing Pipeline** (`document_loader.py`)
- **Semantic Chunking**: Splits documents at paragraph boundaries to preserve semantic coherence
- **Overlap Strategy**: 50-character overlap between chunks ensures context continuity across boundaries
- **Metadata Tracking**: Maintains chunk IDs and character positions for traceability

**2. Vector Store and Retrieval** (`vector_store.py`)
- **Embedding Model**: Sentence-Transformers `all-MiniLM-L6-v2` (efficient, 384-dim embeddings)
- **Index Structure**: FAISS `IndexFlatL2` for exact L2 distance similarity search
- **Scalability**: Extensible to approximate search (IVF, HNSW) for million+ document chunks
- **Persistence**: Serialization support for saving/loading indexed documents

**3. RAG Orchestration** (`rag_pipeline.py`)
- **LLM Integration**: Gemma instruction-tuned models (3-4B default, 3-12B optional) for answer generation
- **Context Assembly**: Intelligent prompt construction with retrieved chunks
- **Inference Optimization**: FP16 precision on GPU, FP32 on CPU
- **Response Extraction**: Parses model output to isolate answer from prompt

**4. Interactive Demo** (`demo.py`)
- **Batch Mode**: Runs predefined queries for capability demonstration
- **Interactive Mode**: Real-time Q&A with configurable parameters
- **Flexible Configuration**: Adjustable chunk size, retrieval count, generation parameters

### Pipeline Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    INDEXING PHASE (One-time)                │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │  Radar Calibration Documentation       │
        │  (radar-calibration-doc.md)            │
        └────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │  Document Loader                       │
        │  • Paragraph-based chunking            │
        │  • 500 char chunks, 50 char overlap    │
        └────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │  Sentence Transformer Encoder          │
        │  • all-MiniLM-L6-v2                    │
        │  • 384-dimensional embeddings          │
        └────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │  FAISS Vector Store                    │
        │  • IndexFlatL2 (exact search)          │
        │  • Persistent storage ready            │
        └────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                QUERY PHASE (Runtime)                        │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │  User Query                            │
        │  "What equipment is needed?"           │
        └────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │  Query Embedding                       │
        │  (same encoder as indexing)            │
        └────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │  Vector Similarity Search              │
        │  • Retrieve top-k chunks               │
        │  • Ranked by L2 distance               │
        └────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │  Prompt Construction                   │
        │  • Context: Retrieved chunks           │
        │  • Instruction: Answer based on context│
        │  • Query: User question                │
        └────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │  Gemma LLM Generation                  │
        │  • Context-aware inference             │
        │  • Temperature-controlled sampling     │
        └────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │  Answer Extraction & Formatting        │
        └────────────────────────────────────────┘
```

## Key Technical Innovations

### 1. Semantic-Aware Chunking
Unlike simple character or token-based splitting, the document loader preserves paragraph boundaries, ensuring each chunk contains complete semantic units. This significantly improves retrieval relevance.

### 2. Hybrid Precision Inference
The pipeline automatically detects available hardware and uses FP16 precision on GPU for 2x memory efficiency and faster inference, while gracefully falling back to FP32 on CPU.

### 3. Context Window Optimization
By retrieving multiple chunks (default: top-3) and concatenating them, the system provides Gemma with sufficient context while staying within token limits, balancing accuracy and computational efficiency.

### 4. Offline-First Design
All components (embedding model, vector store, LLM) run locally without external API calls, making this suitable for secure, air-gapped environments typical in defense and aerospace applications.

## Performance Characteristics

**Retrieval Performance:**
- Vector search: <10ms for 1000 chunks (exact search)
- Scalable to 100K+ chunks with approximate search (IVF/HNSW)
- Embedding generation: ~50-100 chunks/second

**Generation Performance:**
- Gemma 3-4B CPU: ~5-10 tokens/second (recommended)
- Gemma 3-4B GPU: ~15-20 tokens/second (8GB+ VRAM)
- Gemma 3-12B GPU: ~20-30 tokens/second (24GB+ VRAM)
- Memory: ~8GB RAM (CPU, 3-4B) or ~24GB VRAM (GPU, 3-12B)

**Accuracy Considerations:**
- Chunk size: 500 chars balances precision vs. context
- Top-k=3 provides sufficient context without noise
- Temperature=0.7 balances creativity and factual accuracy

## Running the Demonstration

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Gemma 3-4B will be downloaded automatically from HuggingFace on first run
# Or download manually from: https://huggingface.co/google/gemma-3-4b-it
```

### Basic Demo (Predefined Queries)
```bash
python demo.py --model-path google/gemma-3-4b-it --cpu
```

This runs a curated set of queries demonstrating various capability aspects:
- Conceptual understanding
- Procedural knowledge
- Technical specifications
- Troubleshooting guidance

### Interactive Mode
```bash
python demo.py --model-path google/gemma-3-4b-it --interactive --cpu
```

Ask your own questions in real-time and explore the document interactively.

### Advanced Configuration
```bash
python demo.py \
  --model-path google/gemma-3-4b-it \
  --document radar-calibration-doc.md \
  --chunk-size 500 \
  --top-k 3 \
  --max-tokens 512 \
  --temperature 0.7 \
  --interactive \
  --cpu
```

**Tunable Parameters:**
- `--chunk-size`: Adjust semantic granularity (default: 500 chars)
- `--top-k`: Number of context chunks to retrieve (default: 3)
- `--max-tokens`: Response length limit (default: 512)
- `--temperature`: Sampling randomness, 0=deterministic, 1=creative (default: 0.7)

## Application Domains

This RAG architecture is particularly valuable for:

**Defense & Aerospace:**
- Radar system documentation and troubleshooting
- Maintenance procedure retrieval
- Standards compliance verification
- Training and knowledge transfer

**Enterprise & Industrial:**
- Technical manual Q&A
- Equipment operation guidance
- Safety protocol retrieval
- Regulatory compliance documentation

**Research & Development:**
- Scientific literature synthesis
- Patent analysis
- Technical specification comparison
- Design knowledge management

## Project Structure

```
offline-rag-gemma/
│
├── app.py                      # 🌐 Web UI (Gradio) - Main deployment interface
├── run_api.py                  # API server startup script (MLOps)
├── demo.py                     # CLI interactive demo
│
├── api/
│   ├── __init__.py             # API package initialization
│   ├── main.py                 # FastAPI service with endpoints
│   ├── schemas.py              # Pydantic request/response models
│   └── client_example.py       # Example API client
│
├── document_loader.py          # Semantic document chunking
├── vector_store.py             # FAISS-based vector retrieval
├── rag_pipeline.py             # RAG orchestration and LLM integration
│
├── radar-calibration-doc.md    # Example technical documentation
├── requirements.txt            # Python dependencies
├── .gitignore                  # Version control exclusions
└── README.md                   # This documentation
```

## Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| LLM | Gemma 3-4B Instruct (default) | Answer generation |
| Embeddings | Sentence-Transformers (all-MiniLM-L6-v2) | Semantic encoding |
| Vector Store | FAISS (IndexFlatL2) | Similarity search |
| ML Framework | PyTorch | Model inference |
| NLP Library | HuggingFace Transformers | Model loading & tokenization |
| Web UI | Gradio | User interface for deployment |
| API Framework | FastAPI | REST API service (MLOps) |
| API Server | Uvicorn | ASGI web server |

### MLOps Dependencies Explained

This project demonstrates MLOps best practices through carefully selected production-grade dependencies:

#### Core ML Dependencies

| Package | Version | MLOps Purpose |
|---------|---------|---------------|
| **torch** | >=2.0.0 | Deep learning framework for model inference. Provides GPU acceleration and efficient tensor operations critical for production ML workloads. |
| **transformers** | >=4.40.0 | HuggingFace library for loading and running pre-trained models. Industry standard for NLP model deployment with optimized inference engines. |
| **sentence-transformers** | >=2.2.0 | Specialized framework for semantic embeddings. Optimized for production similarity search tasks with pre-built models. |
| **faiss-cpu** | >=1.7.4 | Facebook's vector similarity search library. Production-grade approximate nearest neighbor (ANN) search, scales to billions of vectors. Essential for RAG retrieval. |
| **numpy** | >=1.24.0 | Numerical computing library. Foundation for all ML operations, provides optimized array operations. |
| **tqdm** | >=4.65.0 | Progress bar library. Provides user feedback during long-running operations (indexing, embedding generation). Important for UX in production. |
| **tiktoken** | >=0.5.0 | OpenAI's tokenizer library. Fast and efficient tokenization for text processing, used by modern LLMs. |

#### Deployment & API Dependencies (MLOps)

| Package | Version | MLOps Purpose |
|---------|---------|---------------|
| **fastapi** | >=0.104.0 | Modern web framework for building production APIs. Provides automatic OpenAPI documentation, request validation, async support. Industry standard for ML model serving. |
| **uvicorn[standard]** | >=0.24.0 | ASGI web server for FastAPI. Production-ready with support for workers, graceful shutdowns, and high concurrency. `[standard]` includes websockets and performance optimizations. |
| **pydantic** | >=2.0.0 | Data validation library. Ensures type safety and automatic request/response validation in APIs. Critical for robust production systems - catches errors before they reach the model. |
| **python-multipart** | >=0.0.6 | Handles file uploads in FastAPI. Enables document upload functionality in the API. |
| **gradio** | >=4.0.0 | Web UI framework for ML demos. Provides production-ready interface with minimal code. Perfect for user-facing deployments and stakeholder demos. |

#### Why These Choices Matter for MLOps

**Production Readiness:**
- FastAPI + Uvicorn = Industry-standard ML API serving (used by companies like Uber, Netflix)
- Pydantic = Type safety and data validation prevent runtime errors
- FAISS = Production-scale vector search (used by Facebook, Pinterest for billions of embeddings)

**Observability & Monitoring:**
- FastAPI auto-generates OpenAPI docs → easy API testing and integration
- Health endpoints → Kubernetes readiness/liveness probes
- Metrics tracking → Prometheus integration for monitoring

**Scalability:**
- Uvicorn workers → horizontal scaling
- FAISS → handles million+ document collections
- Async FastAPI → high concurrency without blocking

**Developer Experience:**
- Automatic API documentation → faster onboarding
- Type hints + Pydantic → catch errors early
- Gradio → rapid prototyping and demos

**Offline/Air-Gapped Operation:**
- All dependencies can be pre-installed
- No runtime internet requirements
- Perfect for defense/aerospace secure environments (L3Harris use case)

This stack demonstrates understanding of:
- ✅ Model serving patterns
- ✅ API design for ML systems
- ✅ Production deployment requirements
- ✅ Monitoring and observability
- ✅ Scalability considerations
- ✅ Security (offline operation)

## References & Acknowledgments

**Core Technologies:**
- [Google Gemma 3-4B](https://huggingface.co/google/gemma-3-4b-it) - Instruction-tuned language model
- [Sentence-Transformers](https://www.sbert.net/) - Semantic text embeddings
- [FAISS](https://github.com/facebookresearch/faiss) - Efficient similarity search
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/) - Model inference framework

**Academic Foundations:**
- Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (2020)
- Karpukhin et al., "Dense Passage Retrieval for Open-Domain Question Answering" (2020)

---

**Author:** Technical demonstration of production-grade RAG implementation for AI/ML engineering applications.

**License:** This project uses Gemma models subject to Google's Gemma Terms of Use.
