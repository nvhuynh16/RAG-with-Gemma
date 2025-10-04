"""
RAG Pipeline with Gemma
Retrieval-Augmented Generation using local Gemma model
"""
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from typing import List, Dict, Any
import time
import logging
from prometheus_client import Counter, Histogram, Gauge
from vector_store import VectorStore
from document_loader import DocumentLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
QUERY_COUNT = Counter('rag_query_total', 'Total number of RAG queries')
QUERY_ERRORS = Counter('rag_query_errors_total', 'Total number of query errors')
QUERY_DURATION = Histogram('rag_query_duration_seconds', 'Query duration in seconds')
RETRIEVAL_DURATION = Histogram('rag_retrieval_duration_seconds', 'Retrieval duration in seconds')
GENERATION_DURATION = Histogram('rag_generation_duration_seconds', 'Generation duration in seconds')
CONTEXT_CHUNKS = Histogram('rag_context_chunks', 'Number of context chunks retrieved')
TOKENS_GENERATED = Histogram('rag_tokens_generated', 'Number of tokens generated')
MODEL_MEMORY_USAGE = Gauge('rag_model_memory_mb', 'Model memory usage in MB')


class RAGPipeline:
    """RAG Pipeline with Gemma model"""

    def __init__(
        self,
        model_path: str,
        device: str = "auto",
        use_cpu: bool = False,
        quantize_4bit: bool = False
    ):
        """
        Initialize RAG pipeline

        Args:
            model_path: Path to local Gemma model
            device: Device to run model on ('cpu', 'cuda', or 'auto')
            use_cpu: Force CPU usage (for low memory systems)
            quantize_4bit: Use 4-bit quantization to reduce VRAM usage (~3-4GB for 12B models)
        """
        print("Initializing RAG Pipeline...")

        # Store quantization flag
        self.quantize_4bit = quantize_4bit

        # Determine device
        if use_cpu:
            self.device = "cpu"
            self.gpu_id = None
            print("⚠️  Forced CPU mode (this will be slower but uses less memory)")
        elif device == "auto":
            # Find first CUDA-capable GPU
            cuda_gpu_id = None
            if torch.cuda.is_available():
                num_gpus = torch.cuda.device_count()
                print(f"Detected {num_gpus} GPU(s)")

                # Iterate through GPUs to find first CUDA-capable one
                for gpu_id in range(num_gpus):
                    try:
                        gpu_name = torch.cuda.get_device_name(gpu_id)
                        gpu_mem = torch.cuda.get_device_properties(gpu_id).total_memory / (1024**3)

                        # Check if this is a CUDA GPU (NVIDIA with compute capability)
                        compute_capability = torch.cuda.get_device_capability(gpu_id)

                        if compute_capability[0] >= 3:  # Minimum CUDA compute capability
                            print(f"  GPU {gpu_id}: {gpu_name} ({gpu_mem:.1f}GB) - CUDA capable ✓")
                            if cuda_gpu_id is None:
                                cuda_gpu_id = gpu_id
                        else:
                            print(f"  GPU {gpu_id}: {gpu_name} - Not CUDA capable (compute {compute_capability[0]}.{compute_capability[1]})")
                    except Exception as e:
                        print(f"  GPU {gpu_id}: Error checking GPU - {e}")

                if cuda_gpu_id is not None:
                    self.gpu_id = cuda_gpu_id
                    gpu_mem = torch.cuda.get_device_properties(cuda_gpu_id).total_memory / (1024**3)
                    gpu_name = torch.cuda.get_device_name(cuda_gpu_id)

                    print(f"\n✓ Selected GPU {cuda_gpu_id}: {gpu_name} ({gpu_mem:.1f}GB)")

                    # Check if memory is sufficient
                    if gpu_mem < 3:
                        print(f"⚠️  GPU memory ({gpu_mem:.1f}GB) is very low")
                        print(f"⚠️  Recommended: Use Gemma 3-1B (needs ~2-3GB) or smaller model")
                        print("⚠️  Falling back to CPU for stability")
                        self.device = "cpu"
                        self.gpu_id = None
                    else:
                        self.device = f"cuda:{cuda_gpu_id}"
                        # Set as default device
                        torch.cuda.set_device(cuda_gpu_id)
                else:
                    print("⚠️  No CUDA-capable GPU found, using CPU")
                    self.device = "cpu"
                    self.gpu_id = None
            else:
                print("No CUDA support detected, using CPU")
                self.device = "cpu"
                self.gpu_id = None
        else:
            self.device = device
            self.gpu_id = None

        print(f"Using device: {self.device}")

        # Load Gemma model and tokenizer
        print(f"Loading Gemma model from: {model_path}")
        if self.quantize_4bit:
            print("Using 4-bit quantization (reduces VRAM to ~3-4GB for 12B models)")
        print("This may take a few minutes...")

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

        # Configure 4-bit quantization if requested
        quantization_config = None
        if self.quantize_4bit and self.device != "cpu":
            print("Configuring 4-bit quantization with CPU offloading...")
            print("⚠️  Note: Some layers may be offloaded to CPU if GPU memory is insufficient")
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                llm_int8_enable_fp32_cpu_offload=True  # Enable CPU offloading for low VRAM GPUs
            )

        # Load model with appropriate settings
        if self.device == "cpu":
            print("Loading model on CPU (this will take 3-5 minutes)...")
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                dtype=torch.float32,
                low_cpu_mem_usage=True,
                device_map=None
            )
            self.model = self.model.to(self.device)
        elif self.quantize_4bit:
            print(f"Loading 4-bit quantized model on {self.device}...")
            print("Using 'auto' device mapping - will distribute across GPU/CPU as needed")

            # Check GPU memory to warn user
            if torch.cuda.is_available() and self.gpu_id is not None:
                gpu_mem_gb = torch.cuda.get_device_properties(self.gpu_id).total_memory / (1024**3)
                if gpu_mem_gb < 6:
                    print(f"⚠️  Your GPU has {gpu_mem_gb:.1f}GB VRAM - some layers will be on CPU")
                    print(f"⚠️  This may slow down inference. Consider using --cpu for better quality.")

            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                quantization_config=quantization_config,
                device_map="auto",  # Auto-distribute across GPU/CPU
                low_cpu_mem_usage=True,
                max_memory={0: "3.5GB", "cpu": "16GB"}  # Reserve some GPU memory for activations
            )
        else:
            print(f"Loading model on {self.device}...")
            # Use device_map="auto" which will respect torch.cuda.set_device()
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                dtype=torch.float16,
                device_map="auto",
                low_cpu_mem_usage=True
            )

        self.model.eval()

        # Initialize vector store
        self.vector_store = None

        # Track model memory usage
        if self.device != "cpu" and torch.cuda.is_available():
            memory_allocated = torch.cuda.memory_allocated(self.gpu_id) / (1024**2)  # MB
            MODEL_MEMORY_USAGE.set(memory_allocated)
            logger.info(f"Model memory usage: {memory_allocated:.2f} MB")

        logger.info("RAG Pipeline initialized successfully")
        print("✅ RAG Pipeline initialized successfully")

    def index_document(self, document_path: str, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Load and index a document

        Args:
            document_path: Path to the document
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        print(f"\nIndexing document: {document_path}")

        # Load and chunk document
        loader = DocumentLoader(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = loader.load_and_chunk(document_path)

        # Build vector store
        self.vector_store = VectorStore()
        self.vector_store.build_index(chunks)

        print("Document indexed successfully")

    def index_documents(self, document_paths: List[str], chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Load and index multiple documents

        Args:
            document_paths: List of paths to documents
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        print(f"\nIndexing {len(document_paths)} document(s)...")

        # Load and chunk all documents
        loader = DocumentLoader(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        all_chunks = []

        for doc_path in document_paths:
            print(f"  Loading: {doc_path}")
            chunks = loader.load_and_chunk(doc_path)
            # Add source file metadata to each chunk
            for chunk in chunks:
                chunk['source'] = doc_path
            all_chunks.extend(chunks)
            print(f"    Created {len(chunks)} chunks")

        # Build vector store with all chunks
        self.vector_store = VectorStore()
        self.vector_store.build_index(all_chunks)

        print(f"\n✅ Indexed {len(document_paths)} document(s) with {len(all_chunks)} total chunks")

    def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve relevant context for a query

        Args:
            query: User query
            top_k: Number of chunks to retrieve

        Returns:
            List of relevant chunks
        """
        if self.vector_store is None:
            raise ValueError("No document indexed. Call index_document() first.")

        start_time = time.time()
        results = self.vector_store.search(query, top_k=top_k)
        retrieval_time = time.time() - start_time

        RETRIEVAL_DURATION.observe(retrieval_time)
        CONTEXT_CHUNKS.observe(len(results))
        logger.debug(f"Retrieved {len(results)} chunks in {retrieval_time:.3f}s")

        return [chunk for chunk, distance in results]

    def generate_response(
        self,
        query: str,
        context_chunks: List[Dict],
        max_new_tokens: int = 256,
        temperature: float = 0.7
    ) -> str:
        """
        Generate response using Gemma with retrieved context

        Args:
            query: User query
            context_chunks: Retrieved context chunks
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated response
        """
        start_time = time.time()

        # Construct prompt with context
        context_text = "\n\n".join([chunk['text'] for chunk in context_chunks])

        # Clear prompt format for Gemma models
        prompt = f"""Use the following context to answer the question accurately and concisely.

Context:
{context_text}

Question: {query}

Answer:"""

        # Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        input_length = inputs['input_ids'].shape[1]

        # Generate with balanced parameters for Gemma models
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                top_k=50,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

        # Decode only the generated part (exclude input prompt)
        generated_tokens = outputs[0][input_length:]
        answer = self.tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

        # Clean up formatting artifacts
        answer = answer.lstrip('*#-').strip()

        # Stop at common hallucination patterns (less aggressive for 3-12B)
        stop_phrases = ["Answer:", "Question:", "Context:", "\n\nQuestion"]
        for stop in stop_phrases:
            if stop in answer:
                answer = answer.split(stop)[0].strip()

        generation_time = time.time() - start_time
        num_tokens = len(generated_tokens)

        GENERATION_DURATION.observe(generation_time)
        TOKENS_GENERATED.observe(num_tokens)
        logger.debug(f"Generated {num_tokens} tokens in {generation_time:.3f}s ({num_tokens/generation_time:.1f} tokens/s)")

        return answer

    def query(
        self,
        question: str,
        top_k: int = 3,
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        show_context: bool = False
    ) -> Dict[str, Any]:
        """
        Perform RAG query: retrieve context and generate answer

        Args:
            question: User question
            top_k: Number of context chunks to retrieve
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            show_context: Whether to include retrieved context in response

        Returns:
            Dictionary with answer and optional context
        """
        start_time = time.time()
        QUERY_COUNT.inc()

        try:
            print(f"\nQuery: {question}")
            logger.info(f"Processing query: {question[:100]}...")

            # Retrieve relevant context
            print("Retrieving relevant context...")
            context_chunks = self.retrieve_context(question, top_k=top_k)

            # Generate response
            print("Generating response...")
            answer = self.generate_response(
                question,
                context_chunks,
                max_new_tokens=max_new_tokens,
                temperature=temperature
            )

            query_time = time.time() - start_time
            QUERY_DURATION.observe(query_time)
            logger.info(f"Query completed in {query_time:.3f}s")

            result = {
                "question": question,
                "answer": answer,
                "metadata": {
                    "query_time": query_time,
                    "num_chunks": len(context_chunks)
                }
            }

            if show_context:
                result["context"] = [chunk['text'] for chunk in context_chunks]

            return result

        except Exception as e:
            QUERY_ERRORS.inc()
            logger.error(f"Query failed: {str(e)}", exc_info=True)
            raise


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < 2:
        print("Usage: python rag_pipeline.py <path_to_gemma_model>")
        sys.exit(1)

    model_path = sys.argv[1]

    # Initialize RAG pipeline
    rag = RAGPipeline(model_path=model_path)

    # Index document
    rag.index_document("radar-calibration-doc.md")

    # Example queries
    queries = [
        "What is radar calibration?",
        "What are the main steps in the calibration process?",
        "What equipment is needed for radar calibration?"
    ]

    for query in queries:
        result = rag.query(query, show_context=True)
        print(f"\nQ: {result['question']}")
        print(f"A: {result['answer']}")
        print("-" * 80)
