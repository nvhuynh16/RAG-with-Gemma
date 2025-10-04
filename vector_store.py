"""
Vector Store Module
Creates embeddings and performs similarity search using FAISS
"""
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple, Any
import pickle
import os


class VectorStore:
    """Vector store for embedding-based retrieval"""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize vector store with embedding model

        Args:
            model_name: Name of the sentence transformer model
        """
        print(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = None
        self.dimension = None

    def create_embeddings(self, chunks: List[Dict[str, Any]]) -> np.ndarray:
        """
        Create embeddings for document chunks

        Args:
            chunks: List of document chunks

        Returns:
            Numpy array of embeddings
        """
        texts = [chunk['text'] for chunk in chunks]
        print(f"Creating embeddings for {len(texts)} chunks...")

        embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        return embeddings

    def build_index(self, chunks: List[Dict[str, Any]]):
        """
        Build FAISS index from document chunks

        Args:
            chunks: List of document chunks
        """
        self.chunks = chunks
        embeddings = self.create_embeddings(chunks)

        self.dimension = embeddings.shape[1]

        # Create FAISS index (using L2 distance)
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings.astype('float32'))

        print(f"Built FAISS index with {self.index.ntotal} vectors")

    def search(self, query: str, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search for most relevant chunks

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of (chunk, distance) tuples
        """
        if self.index is None:
            raise ValueError("Index not built. Call build_index() first.")

        # Embed the query
        query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)

        # Search the index
        distances, indices = self.index.search(query_embedding.astype('float32'), top_k)

        # Return chunks with their distances
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            results.append((self.chunks[idx], float(dist)))

        return results

    def save(self, path: str):
        """
        Save vector store to disk

        Args:
            path: Directory path to save the index
        """
        os.makedirs(path, exist_ok=True)

        # Save FAISS index
        faiss.write_index(self.index, os.path.join(path, "index.faiss"))

        # Save chunks
        with open(os.path.join(path, "chunks.pkl"), 'wb') as f:
            pickle.dump(self.chunks, f)

        print(f"Saved vector store to {path}")

    def load(self, path: str):
        """
        Load vector store from disk

        Args:
            path: Directory path to load the index from
        """
        # Load FAISS index
        self.index = faiss.read_index(os.path.join(path, "index.faiss"))

        # Load chunks
        with open(os.path.join(path, "chunks.pkl"), 'rb') as f:
            self.chunks = pickle.load(f)

        self.dimension = self.index.d

        print(f"Loaded vector store from {path} ({self.index.ntotal} vectors)")


if __name__ == "__main__":
    # Test the vector store
    from document_loader import DocumentLoader

    loader = DocumentLoader(chunk_size=500, chunk_overlap=50)
    chunks = loader.load_and_chunk("radar-calibration-doc.md")

    vector_store = VectorStore()
    vector_store.build_index(chunks)

    # Test search
    query = "What is radar calibration?"
    results = vector_store.search(query, top_k=3)

    print(f"\nSearch results for: '{query}'")
    for i, (chunk, distance) in enumerate(results):
        print(f"\n--- Result {i+1} (distance: {distance:.4f}) ---")
        print(chunk['text'][:200] + "...")
