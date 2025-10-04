"""
MLflow Experiment Tracking for RAG Pipeline
Tracks experiments, parameters, metrics, and models
"""
import argparse
import os
import json
from datetime import datetime
from typing import Dict, Any

import mlflow
import mlflow.pytorch
from rag_pipeline import RAGPipeline


class MLflowExperimentTracker:
    """Track RAG experiments with MLflow"""

    def __init__(self, tracking_uri: str = "http://localhost:5000", experiment_name: str = "rag-gemma"):
        """Initialize MLflow tracking"""
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)

        self.experiment = mlflow.get_experiment_by_name(experiment_name)
        print(f"MLflow Tracking URI: {tracking_uri}")
        print(f"Experiment: {experiment_name} (ID: {self.experiment.experiment_id})")

    def run_experiment(
        self,
        model_path: str,
        document_path: str,
        test_queries: list,
        run_name: str = None,
        use_cpu: bool = False,
        quantize: bool = False,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        top_k: int = 3,
        max_tokens: int = 256,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Run tracked experiment"""

        # Generate run name if not provided
        if run_name is None:
            device = "cpu" if use_cpu else "gpu"
            quant = "4bit" if quantize else "fp16"
            run_name = f"{model_path.split('/')[-1]}_{device}_{quant}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        with mlflow.start_run(run_name=run_name):
            print(f"\nStarting MLflow run: {run_name}")

            # Log parameters
            params = {
                "model_path": model_path,
                "device": "cpu" if use_cpu else "cuda",
                "quantization": "4bit" if quantize else "none",
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "top_k": top_k,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "document": document_path
            }

            for key, value in params.items():
                mlflow.log_param(key, value)

            print(f"Logged {len(params)} parameters")

            # Initialize pipeline
            print("\nInitializing RAG pipeline...")
            import time
            start_init = time.time()

            pipeline = RAGPipeline(
                model_path=model_path,
                use_cpu=use_cpu,
                quantize_4bit=quantize
            )

            init_time = time.time() - start_init
            mlflow.log_metric("init_time_seconds", init_time)

            # Index document
            print(f"Indexing document: {document_path}")
            start_index = time.time()

            pipeline.index_document(
                document_path=document_path,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )

            index_time = time.time() - start_index
            mlflow.log_metric("index_time_seconds", index_time)

            # Get index stats
            num_chunks = len(pipeline.vector_store.chunks)
            mlflow.log_metric("num_chunks", num_chunks)

            # Run queries and collect metrics
            print(f"\nRunning {len(test_queries)} test queries...")
            query_times = []
            token_counts = []

            for i, query in enumerate(test_queries, 1):
                print(f"  [{i}/{len(test_queries)}] {query[:50]}...")

                start_query = time.time()
                result = pipeline.query(
                    question=query,
                    top_k=top_k,
                    max_new_tokens=max_tokens,
                    temperature=temperature
                )
                query_time = time.time() - start_query

                query_times.append(query_time)
                token_counts.append(len(result["answer"].split()))

            # Calculate and log aggregate metrics
            avg_query_time = sum(query_times) / len(query_times)
            avg_tokens = sum(token_counts) / len(token_counts)
            throughput = 1.0 / avg_query_time

            metrics = {
                "avg_query_time_seconds": avg_query_time,
                "avg_query_time_ms": avg_query_time * 1000,
                "max_query_time_seconds": max(query_times),
                "min_query_time_seconds": min(query_times),
                "avg_tokens_per_response": avg_tokens,
                "tokens_per_second": avg_tokens / avg_query_time,
                "throughput_qps": throughput,
                "total_queries": len(test_queries)
            }

            for key, value in metrics.items():
                mlflow.log_metric(key, value)

            print(f"\nLogged {len(metrics)} metrics")

            # Log query results as artifact
            results_data = {
                "run_name": run_name,
                "timestamp": datetime.utcnow().isoformat(),
                "parameters": params,
                "metrics": metrics,
                "queries": [
                    {
                        "question": q,
                        "time_seconds": t,
                        "tokens": c
                    }
                    for q, t, c in zip(test_queries, query_times, token_counts)
                ]
            }

            # Save results to temp file
            results_file = f"/tmp/mlflow_results_{run_name}.json"
            with open(results_file, 'w') as f:
                json.dump(results_data, f, indent=2)

            mlflow.log_artifact(results_file, "results")
            print(f"Logged results artifact")

            # Log model info (metadata only, not full weights)
            model_info = {
                "model_path": model_path,
                "device": params["device"],
                "quantization": params["quantization"]
            }

            model_info_file = f"/tmp/model_info_{run_name}.json"
            with open(model_info_file, 'w') as f:
                json.dump(model_info, f, indent=2)

            mlflow.log_artifact(model_info_file, "model")
            print(f"Logged model info")

            # Log tags
            mlflow.set_tag("model_family", "gemma")
            mlflow.set_tag("task", "rag")
            mlflow.set_tag("domain", "radar_calibration")

            print(f"\nMLflow run completed: {mlflow.active_run().info.run_id}")
            print(f"View at: {mlflow.get_tracking_uri()}/#/experiments/{self.experiment.experiment_id}")

            return {
                "run_id": mlflow.active_run().info.run_id,
                "metrics": metrics,
                "parameters": params
            }


def compare_runs(tracking_uri: str = "http://localhost:5000", experiment_name: str = "rag-gemma"):
    """Compare all runs in experiment"""
    mlflow.set_tracking_uri(tracking_uri)

    # Get experiment
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if not experiment:
        print(f"Experiment '{experiment_name}' not found")
        return

    # Get all runs
    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])

    if runs.empty:
        print(f"No runs found in experiment '{experiment_name}'")
        return

    print(f"\n{'='*80}")
    print(f"Experiment: {experiment_name}")
    print(f"{'='*80}")

    # Display summary
    print(f"\n{len(runs)} runs found:\n")

    # Sort by metric (e.g., avg_query_time_ms)
    if "metrics.avg_query_time_ms" in runs.columns:
        runs = runs.sort_values("metrics.avg_query_time_ms")

    # Display top runs
    for idx, run in runs.head(10).iterrows():
        print(f"Run: {run['tags.mlflow.runName']}")
        print(f"  ID: {run['run_id'][:8]}...")
        print(f"  Model: {run.get('params.model_path', 'N/A')}")
        print(f"  Device: {run.get('params.device', 'N/A')}")
        print(f"  Avg Query Time: {run.get('metrics.avg_query_time_ms', 'N/A'):.1f} ms")
        print(f"  Throughput: {run.get('metrics.throughput_qps', 'N/A'):.2f} qps")
        print(f"  Tokens/sec: {run.get('metrics.tokens_per_second', 'N/A'):.1f}")
        print()


def main():
    parser = argparse.ArgumentParser(description="MLflow Experiment Tracking for RAG")
    parser.add_argument("--tracking-uri", type=str, default="http://localhost:5000",
                        help="MLflow tracking URI")
    parser.add_argument("--experiment-name", type=str, default="rag-gemma",
                        help="MLflow experiment name")
    parser.add_argument("--model-path", type=str, default="google/gemma-3-4b-it",
                        help="Path to Gemma model")
    parser.add_argument("--document", type=str, default="radar-calibration-doc.md",
                        help="Document to index")
    parser.add_argument("--run-name", type=str, default=None,
                        help="Custom run name")
    parser.add_argument("--cpu", action="store_true",
                        help="Force CPU mode")
    parser.add_argument("--quantize", action="store_true",
                        help="Use 4-bit quantization")
    parser.add_argument("--compare", action="store_true",
                        help="Compare all runs instead of running new experiment")

    args = parser.parse_args()

    # Compare mode
    if args.compare:
        compare_runs(args.tracking_uri, args.experiment_name)
        return

    # Run experiment mode
    test_queries = [
        "What is radar calibration?",
        "What are the main steps in the calibration process?",
        "What equipment is needed for radar calibration?",
        "What are common challenges in radar calibration?",
        "How do you verify calibration accuracy?"
    ]

    tracker = MLflowExperimentTracker(
        tracking_uri=args.tracking_uri,
        experiment_name=args.experiment_name
    )

    result = tracker.run_experiment(
        model_path=args.model_path,
        document_path=args.document,
        test_queries=test_queries,
        run_name=args.run_name,
        use_cpu=args.cpu,
        quantize=args.quantize
    )

    print("\n" + "="*80)
    print("EXPERIMENT SUMMARY")
    print("="*80)
    print(f"\nRun ID: {result['run_id']}")
    print(f"\nKey Metrics:")
    for key, value in result['metrics'].items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
