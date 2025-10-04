"""
Example client for RAG API
Demonstrates how to interact with the API endpoints
"""
import requests
import json


API_BASE_URL = "http://localhost:8000"


def check_health():
    """Check API health status"""
    print("\n=== Health Check ===")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()


def query_rag(question: str, include_context: bool = False):
    """Query the RAG system"""
    print(f"\n=== Query: {question} ===")

    payload = {
        "question": question,
        "top_k": 3,
        "max_tokens": 256,
        "temperature": 0.7,
        "include_context": include_context
    }

    response = requests.post(f"{API_BASE_URL}/query", json=payload)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\nQuestion: {result['question']}")
        print(f"Answer: {result['answer']}")
        print(f"\nMetadata:")
        print(f"  Response Time: {result['metadata']['response_time_ms']}ms")
        print(f"  Temperature: {result['metadata']['temperature']}")
        print(f"  Top-k: {result['metadata']['top_k']}")

        if result.get('context'):
            print(f"\nRetrieved Context:")
            for i, ctx in enumerate(result['context'], 1):
                print(f"\n  Chunk {i}:")
                print(f"  {ctx[:200]}...")
    else:
        print(f"Error: {response.json()}")

    return response.json() if response.status_code == 200 else None


def get_metrics():
    """Get service metrics"""
    print("\n=== Service Metrics ===")
    response = requests.get(f"{API_BASE_URL}/metrics")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()


def main():
    """Run example queries"""
    print("=" * 80)
    print("RAG API Client Example")
    print("=" * 80)

    # Check health
    health = check_health()

    if not health.get("model_loaded"):
        print("\nERROR: Model not loaded. Set GEMMA_MODEL_PATH environment variable and restart the API.")
        return

    if not health.get("document_indexed"):
        print("\nERROR: No document indexed. The API should auto-index on startup.")
        return

    # Example queries
    queries = [
        "What is radar calibration?",
        "What are the main steps in the calibration process?",
        "What equipment is needed for radar calibration?",
    ]

    for query in queries:
        query_rag(query, include_context=False)

    # Example with context
    print("\n" + "=" * 80)
    print("Example with Retrieved Context")
    print("=" * 80)
    query_rag("What are common calibration challenges?", include_context=True)

    # Get metrics
    get_metrics()


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\nERROR: Cannot connect to API. Make sure the API is running:")
        print("  python run_api.py --model-path google/gemma-3-4b-it")
