"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class QueryRequest(BaseModel):
    """Request model for RAG query"""
    question: str = Field(..., description="Question to ask the RAG system", min_length=1)
    top_k: int = Field(3, description="Number of context chunks to retrieve", ge=1, le=10)
    max_tokens: int = Field(256, description="Maximum tokens to generate", ge=50, le=2048)
    temperature: float = Field(0.7, description="Sampling temperature", ge=0.0, le=2.0)
    include_context: bool = Field(False, description="Include retrieved context in response")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is radar calibration?",
                "top_k": 3,
                "max_tokens": 256,
                "temperature": 0.7,
                "include_context": False
            }
        }


class QueryResponse(BaseModel):
    """Response model for RAG query"""
    question: str = Field(..., description="The question that was asked")
    answer: str = Field(..., description="Generated answer from RAG pipeline")
    context: Optional[List[str]] = Field(None, description="Retrieved context chunks (if requested)")
    metadata: dict = Field(..., description="Additional metadata about the query")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is radar calibration?",
                "answer": "Radar calibration is the systematic process of adjusting and verifying radar system measurements...",
                "context": None,
                "metadata": {
                    "top_k": 3,
                    "max_tokens": 256,
                    "temperature": 0.7,
                    "response_time_ms": 2345.67
                }
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether the model is loaded")
    document_indexed: bool = Field(..., description="Whether the document is indexed")
    index_size: Optional[int] = Field(None, description="Number of chunks in the index")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "model_loaded": True,
                "document_indexed": True,
                "index_size": 130
            }
        }


class IndexRequest(BaseModel):
    """Request to index new document(s)"""
    document_paths: List[str] = Field(..., description="Path(s) to document(s) to index", min_length=1)
    chunk_size: int = Field(500, description="Chunk size for splitting", ge=100, le=2000)
    chunk_overlap: int = Field(50, description="Overlap between chunks", ge=0, le=500)

    class Config:
        json_schema_extra = {
            "example": {
                "document_paths": ["radar-calibration-doc.md"],
                "chunk_size": 500,
                "chunk_overlap": 50
            }
        }


class IndexResponse(BaseModel):
    """Response from indexing operation"""
    status: str = Field(..., description="Indexing status")
    document_paths: List[str] = Field(..., description="Paths to indexed documents")
    chunks_created: int = Field(..., description="Number of chunks created from all documents")
    index_size: int = Field(..., description="Total size of index")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "document_paths": ["radar-calibration-doc.md"],
                "chunks_created": 130,
                "index_size": 130
            }
        }


class MetricsResponse(BaseModel):
    """Prometheus-style metrics response"""
    total_queries: int = Field(..., description="Total number of queries processed")
    average_response_time_ms: float = Field(..., description="Average response time in milliseconds")
    total_errors: int = Field(..., description="Total number of errors")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")

    class Config:
        json_schema_extra = {
            "example": {
                "total_queries": 42,
                "average_response_time_ms": 1234.56,
                "total_errors": 0,
                "uptime_seconds": 3600.0
            }
        }
