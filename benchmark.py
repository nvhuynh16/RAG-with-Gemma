"""
Performance Benchmark Script for RAG Pipeline
Measures throughput, latency, and resource usage
"""
import argparse
import time
import json
import sys
from typing import List, Dict, Any
import statistics
from datetime import datetime
import psutil
import torch

from rag_pipeline import RAGPipeline


class PerformanceBenchmark:
    """Benchmark RAG pipeline performance"""

    def __init__(self, model_path: str, use_cpu: bool = False, quantize: bool = False):
        """Initialize benchmark"""
        print("=" * 60)
        print("RAG Pipeline Performance Benchmark")
        print("=" * 60)

        self.model_path = model_path
        self.use_cpu = use_cpu
        self.quantize = quantize

        # Initialize pipeline
        print(f"\nInitializing RAG pipeline...")
        start_init = time.time()
        self.pipeline = RAGPipeline(
            model_path=model_path,
            use_cpu=use_cpu,
            quantize_4bit=quantize
        )
        self.init_time = time.time() - start_init

        # Track resource usage
        self.process = psutil.Process()

    def prepare_data(self, document_path: str = "radar-calibration-doc.md"):
        """Index test document"""
        print(f"\nIndexing document: {document_path}")
        start_index = time.time()
        self.pipeline.index_document(document_path)
        self.index_time = time.time() - start_index
        print(f"Indexing completed in {self.index_time:.2f}s")

    def run_query_benchmark(
        self,
        queries: List[str],
        top_k: int = 3,
        max_tokens: int = 256,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Run query benchmark"""
        print(f"\nRunning query benchmark ({len(queries)} queries)...")

        results = {
            "query_times": [],
            "retrieval_times": [],
            "generation_times": [],
            "tokens_generated": [],
            "memory_usage_mb": []
        }

        for i, query in enumerate(queries, 1):
            print(f"\n[{i}/{len(queries)}] Query: {query[:60]}...")

            # Track memory before query
            mem_before = self.process.memory_info().rss / (1024 ** 2)  # MB

            # Run query with timing
            start_query = time.time()
            result = self.pipeline.query(
                question=query,
                top_k=top_k,
                max_new_tokens=max_tokens,
                temperature=temperature
            )
            query_time = time.time() - start_query

            # Track memory after query
            mem_after = self.process.memory_info().rss / (1024 ** 2)  # MB

            # Extract metadata if available
            metadata = result.get("metadata", {})
            query_time_meta = metadata.get("query_time", query_time)

            results["query_times"].append(query_time)
            results["memory_usage_mb"].append(mem_after - mem_before)

            # Track tokens if available
            answer_tokens = len(result["answer"].split())
            results["tokens_generated"].append(answer_tokens)

            print(f"  Time: {query_time:.2f}s | Tokens: {answer_tokens} | Memory Δ: {mem_after - mem_before:.1f}MB")

        return results

    def calculate_statistics(self, data: List[float]) -> Dict[str, float]:
        """Calculate statistical metrics"""
        if not data:
            return {}

        return {
            "min": min(data),
            "max": max(data),
            "mean": statistics.mean(data),
            "median": statistics.median(data),
            "stdev": statistics.stdev(data) if len(data) > 1 else 0,
            "p50": statistics.median(data),
            "p95": sorted(data)[int(len(data) * 0.95)] if len(data) > 1 else data[0],
            "p99": sorted(data)[int(len(data) * 0.99)] if len(data) > 1 else data[0]
        }

    def generate_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate benchmark report"""
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "configuration": {
                "model": self.model_path,
                "device": "CPU" if self.use_cpu else "GPU",
                "quantization": "4-bit" if self.quantize else "None",
                "init_time_seconds": round(self.init_time, 2),
                "index_time_seconds": round(self.index_time, 2)
            },
            "performance": {
                "num_queries": len(results["query_times"]),
                "throughput_qps": round(1.0 / statistics.mean(results["query_times"]), 2),
                "latency": {
                    "query_time_seconds": self.calculate_statistics(results["query_times"])
                },
                "tokens": {
                    "avg_tokens_per_query": round(statistics.mean(results["tokens_generated"]), 1),
                    "tokens_per_second": round(
                        sum(results["tokens_generated"]) / sum(results["query_times"]), 1
                    )
                },
                "memory": {
                    "avg_increase_mb": round(statistics.mean(results["memory_usage_mb"]), 1),
                    "peak_increase_mb": round(max(results["memory_usage_mb"]), 1)
                }
            }
        }

        # Add GPU memory if available
        if not self.use_cpu and torch.cuda.is_available():
            report["performance"]["gpu"] = {
                "memory_allocated_mb": round(torch.cuda.memory_allocated() / (1024**2), 1),
                "memory_reserved_mb": round(torch.cuda.memory_reserved() / (1024**2), 1)
            }

        return report

    def print_report(self, report: Dict[str, Any]):
        """Print formatted report"""
        print("\n" + "=" * 60)
        print("BENCHMARK RESULTS")
        print("=" * 60)

        print(f"\nConfiguration:")
        print(f"  Model: {report['configuration']['model']}")
        print(f"  Device: {report['configuration']['device']}")
        print(f"  Quantization: {report['configuration']['quantization']}")
        print(f"  Init Time: {report['configuration']['init_time_seconds']}s")
        print(f"  Index Time: {report['configuration']['index_time_seconds']}s")

        perf = report["performance"]
        print(f"\nPerformance:")
        print(f"  Queries Tested: {perf['num_queries']}")
        print(f"  Throughput: {perf['throughput_qps']} queries/sec")

        latency = perf["latency"]["query_time_seconds"]
        print(f"\nLatency (Query Time):")
        print(f"  Mean: {latency['mean']*1000:.0f} ms")
        print(f"  Median (P50): {latency['p50']*1000:.0f} ms")
        print(f"  P95: {latency['p95']*1000:.0f} ms")
        print(f"  P99: {latency['p99']*1000:.0f} ms")
        print(f"  Min: {latency['min']*1000:.0f} ms")
        print(f"  Max: {latency['max']*1000:.0f} ms")

        tokens = perf["tokens"]
        print(f"\nToken Generation:")
        print(f"  Avg Tokens/Query: {tokens['avg_tokens_per_query']}")
        print(f"  Tokens/Second: {tokens['tokens_per_second']}")

        memory = perf["memory"]
        print(f"\nMemory Usage:")
        print(f"  Avg Increase: {memory['avg_increase_mb']} MB")
        print(f"  Peak Increase: {memory['peak_increase_mb']} MB")

        if "gpu" in perf:
            gpu = perf["gpu"]
            print(f"\nGPU Memory:")
            print(f"  Allocated: {gpu['memory_allocated_mb']} MB")
            print(f"  Reserved: {gpu['memory_reserved_mb']} MB")

        print("\n" + "=" * 60)

    def run(self, document_path: str, queries: List[str], output_file: str = None):
        """Run full benchmark"""
        # Prepare data
        self.prepare_data(document_path)

        # Run queries
        results = self.run_query_benchmark(queries)

        # Generate report
        report = self.generate_report(results)

        # Print report
        self.print_report(report)

        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\nResults saved to: {output_file}")

        return report


def main():
    parser = argparse.ArgumentParser(description="Benchmark RAG Pipeline Performance")
    parser.add_argument("--model-path", type=str, default="google/gemma-3-4b-it",
                        help="Path to Gemma model")
    parser.add_argument("--document", type=str, default="radar-calibration-doc.md",
                        help="Document to index")
    parser.add_argument("--cpu", action="store_true",
                        help="Force CPU mode")
    parser.add_argument("--quantize", action="store_true",
                        help="Use 4-bit quantization")
    parser.add_argument("--output", type=str, default=None,
                        help="Output file for results (JSON)")
    parser.add_argument("--num-queries", type=int, default=10,
                        help="Number of test queries")

    args = parser.parse_args()

    # Test queries
    test_queries = [
        "What is radar calibration?",
        "What are the main steps in the calibration process?",
        "What equipment is needed for radar calibration?",
        "What are common challenges in radar calibration?",
        "How do you verify calibration accuracy?",
        "What is the purpose of antenna alignment?",
        "Explain the frequency calibration procedure.",
        "What safety precautions are needed?",
        "How often should radar systems be calibrated?",
        "What documentation is required for calibration?"
    ][:args.num_queries]

    # Run benchmark
    benchmark = PerformanceBenchmark(
        model_path=args.model_path,
        use_cpu=args.cpu,
        quantize=args.quantize
    )

    benchmark.run(
        document_path=args.document,
        queries=test_queries,
        output_file=args.output
    )


if __name__ == "__main__":
    main()
