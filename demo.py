"""
RAG Demo Script
Interactive demonstration of RAG pipeline with Gemma
"""
import argparse
from rag_pipeline import RAGPipeline


def main():
    parser = argparse.ArgumentParser(description="RAG Demo with Gemma")
    parser.add_argument(
        "--model-path",
        type=str,
        required=True,
        help="Path to local Gemma model directory"
    )
    parser.add_argument(
        "--document",
        type=str,
        nargs='+',
        default=["radar-calibration-doc.md"],
        help="Path(s) to document(s) to index (supports multiple files)"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Chunk size for document splitting (default: 500)"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of context chunks to retrieve (default: 3)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=256,
        help="Maximum tokens to generate (default: 256)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature (default: 0.7)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Use CPU mode (recommended for most users)"
    )
    parser.add_argument(
        "--quantize",
        action="store_true",
        help="Use 4-bit quantization (legacy option, may have compatibility issues)"
    )

    args = parser.parse_args()

    print("=" * 80)
    print("RAG Pipeline Demo with Gemma")
    print("=" * 80)

    # Initialize RAG pipeline
    rag = RAGPipeline(model_path=args.model_path, use_cpu=args.cpu, quantize_4bit=args.quantize)

    # Index document(s)
    rag.index_documents(
        document_paths=args.document,
        chunk_size=args.chunk_size
    )

    if args.interactive:
        # Interactive mode
        print("\n" + "=" * 80)
        print("Interactive Mode - Type 'quit' or 'exit' to stop")
        print("=" * 80)

        while True:
            try:
                question = input("\nYour question: ").strip()

                if question.lower() in ['quit', 'exit', 'q']:
                    print("Exiting...")
                    break

                if not question:
                    continue

                result = rag.query(
                    question,
                    top_k=args.top_k,
                    max_new_tokens=args.max_tokens,
                    temperature=args.temperature,
                    show_context=False
                )

                print(f"\nAnswer: {result['answer']}")
                print("-" * 80)

            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"\nError: {e}")
                continue

    else:
        # Run predefined demo questions
        demo_questions = [
            "What is radar calibration?",
            "What are the main steps in the calibration process?",
            "What equipment is needed for radar calibration?",
            "What are common calibration challenges?",
            "How often should radar systems be calibrated?"
        ]

        print("\n" + "=" * 80)
        print("Running Demo Questions")
        print("=" * 80)

        for i, question in enumerate(demo_questions, 1):
            print(f"\n[Question {i}/{len(demo_questions)}]")

            result = rag.query(
                question,
                top_k=args.top_k,
                max_new_tokens=args.max_tokens,
                temperature=args.temperature,
                show_context=False
            )

            print(f"\nQ: {result['question']}")
            print(f"A: {result['answer']}")
            print("-" * 80)

        print("\nDemo completed!")
        print("\nTo run in interactive mode, use: python demo.py --model-path <path> --interactive")


if __name__ == "__main__":
    main()
