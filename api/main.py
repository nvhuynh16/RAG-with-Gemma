"""
FastAPI Service for Offline RAG Pipeline
Production-ready REST API for document Q&A
"""
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import uvicorn

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag_pipeline import RAGPipeline
from api.schemas import (
    QueryRequest,
    QueryResponse,
    HealthResponse,
    IndexRequest,
    IndexResponse,
    MetricsResponse
)


# Initialize FastAPI app
app = FastAPI(
    title="Offline RAG Pipeline API",
    description="Production-ready Retrieval-Augmented Generation API using Gemma LLM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global state
class AppState:
    """Application state container"""
    def __init__(self):
        self.rag_pipeline: Optional[RAGPipeline] = None
        self.model_path: Optional[str] = None
        self.document_indexed: bool = False
        self.index_size: int = 0
        self.total_queries: int = 0
        self.total_errors: int = 0
        self.response_times: list = []
        self.start_time: float = time.time()


state = AppState()


@app.on_event("startup")
async def startup_event():
    """Initialize the RAG pipeline on startup"""
    # Get model path from environment variable
    model_path = os.getenv("GEMMA_MODEL_PATH")
    document_paths_str = os.getenv("DOCUMENT_PATH", "radar-calibration-doc.md")

    # Parse multiple document paths (pipe-delimited)
    document_paths = document_paths_str.split("|") if document_paths_str else []

    if not model_path:
        print("WARNING: GEMMA_MODEL_PATH not set. Model will need to be loaded via /initialize endpoint")
        return

    try:
        print(f"Initializing RAG Pipeline with model: {model_path}")
        state.rag_pipeline = RAGPipeline(model_path=model_path)
        state.model_path = model_path

        # Auto-index documents if they exist
        existing_docs = [doc for doc in document_paths if os.path.exists(doc)]
        if existing_docs:
            print(f"Auto-indexing {len(existing_docs)} document(s)")
            state.rag_pipeline.index_documents(existing_docs)
            state.document_indexed = True
            state.index_size = len(state.rag_pipeline.vector_store.chunks) if state.rag_pipeline.vector_store else 0
            print(f"Documents indexed successfully. Index size: {state.index_size}")
        else:
            print(f"No valid documents found in: {document_paths}")

    except Exception as e:
        print(f"ERROR during startup: {e}")
        print("Service will start but RAG pipeline needs manual initialization")


@app.get("/", tags=["General"])
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Offline RAG Pipeline API",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if state.rag_pipeline else "initializing",
        model_loaded=state.rag_pipeline is not None,
        document_indexed=state.document_indexed,
        index_size=state.index_size if state.document_indexed else None
    )


@app.get("/metrics", tags=["Monitoring"])
async def get_metrics():
    """Get Prometheus metrics"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.get("/metrics/summary", response_model=MetricsResponse, tags=["Monitoring"])
async def get_metrics_summary():
    """Get human-readable service metrics summary"""
    avg_response_time = sum(state.response_times) / len(state.response_times) if state.response_times else 0.0
    uptime = time.time() - state.start_time

    return MetricsResponse(
        total_queries=state.total_queries,
        average_response_time_ms=avg_response_time,
        total_errors=state.total_errors,
        uptime_seconds=uptime
    )


@app.post("/initialize", tags=["Management"])
async def initialize_model(model_path: str):
    """Manually initialize the RAG pipeline with a specific model path"""
    try:
        print(f"Initializing RAG Pipeline with model: {model_path}")
        state.rag_pipeline = RAGPipeline(model_path=model_path)
        state.model_path = model_path

        return {
            "status": "success",
            "message": "RAG pipeline initialized successfully",
            "model_path": model_path
        }
    except Exception as e:
        state.total_errors += 1
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize model: {str(e)}"
        )


@app.post("/index", response_model=IndexResponse, tags=["Management"])
async def index_document(request: IndexRequest):
    """Index new document(s)"""
    if not state.rag_pipeline:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG pipeline not initialized. Call /initialize first or set GEMMA_MODEL_PATH environment variable."
        )

    try:
        # Check if all documents exist
        missing_docs = [doc for doc in request.document_paths if not os.path.exists(doc)]
        if missing_docs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Documents not found: {', '.join(missing_docs)}"
            )

        # Index the documents
        print(f"Indexing {len(request.document_paths)} document(s)")
        state.rag_pipeline.index_documents(
            document_paths=request.document_paths,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )

        state.document_indexed = True
        state.index_size = len(state.rag_pipeline.vector_store.chunks)

        return IndexResponse(
            status="success",
            document_paths=request.document_paths,
            chunks_created=state.index_size,
            index_size=state.index_size
        )

    except HTTPException:
        raise
    except Exception as e:
        state.total_errors += 1
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to index document: {str(e)}"
        )


@app.post("/query", response_model=QueryResponse, tags=["RAG"])
async def query_rag(request: QueryRequest):
    """
    Query the RAG system with a question

    This endpoint performs the full RAG pipeline:
    1. Retrieves relevant context chunks from the indexed document
    2. Generates an answer using Gemma LLM with the retrieved context
    """
    # Check if pipeline is ready
    if not state.rag_pipeline:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG pipeline not initialized. Call /initialize first or set GEMMA_MODEL_PATH environment variable."
        )

    if not state.document_indexed:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No document indexed. Call /index endpoint first."
        )

    # Track request
    start_time = time.time()

    try:
        # Execute RAG query
        result = state.rag_pipeline.query(
            question=request.question,
            top_k=request.top_k,
            max_new_tokens=request.max_tokens,
            temperature=request.temperature,
            show_context=request.include_context
        )

        # Calculate response time
        response_time_ms = (time.time() - start_time) * 1000
        state.response_times.append(response_time_ms)
        state.total_queries += 1

        # Keep only last 100 response times for metrics
        if len(state.response_times) > 100:
            state.response_times = state.response_times[-100:]

        # Build response
        return QueryResponse(
            question=result["question"],
            answer=result["answer"],
            context=result.get("context") if request.include_context else None,
            metadata={
                "top_k": request.top_k,
                "max_tokens": request.max_tokens,
                "temperature": request.temperature,
                "response_time_ms": round(response_time_ms, 2),
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    except Exception as e:
        state.total_errors += 1
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query failed: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    state.total_errors += 1
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error": str(exc)
        }
    )


def main():
    """Run the FastAPI server"""
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Set to True for development
        log_level="info"
    )


if __name__ == "__main__":
    main()
