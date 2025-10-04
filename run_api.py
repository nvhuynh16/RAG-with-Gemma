#!/usr/bin/env python3
"""
Startup script for RAG API Service
"""
import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="Start the RAG API Service")
    parser.add_argument(
        "--model-path",
        type=str,
        help="Path to Gemma model (can also use GEMMA_MODEL_PATH env var)"
    )
    parser.add_argument(
        "--document",
        type=str,
        nargs='+',
        default=["radar-calibration-doc.md"],
        help="Path(s) to document(s) to auto-index on startup (supports multiple files)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )

    args = parser.parse_args()

    # Set environment variables
    if args.model_path:
        os.environ["GEMMA_MODEL_PATH"] = args.model_path

    # Join multiple document paths with pipe delimiter
    os.environ["DOCUMENT_PATH"] = "|".join(args.document)

    # Import after setting environment variables
    import uvicorn

    print("=" * 80)
    print("Starting RAG API Service")
    print("=" * 80)
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Model Path: {os.getenv('GEMMA_MODEL_PATH', 'Not set - will need manual initialization')}")
    print(f"Document: {args.document}")
    print(f"Reload: {args.reload}")
    print("=" * 80)
    print(f"\nAPI Documentation: http://{args.host}:{args.port}/docs")
    print(f"Health Check: http://{args.host}:{args.port}/health")
    print(f"Metrics: http://{args.host}:{args.port}/metrics")
    print("=" * 80)

    # Start the server
    uvicorn.run(
        "api.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()
