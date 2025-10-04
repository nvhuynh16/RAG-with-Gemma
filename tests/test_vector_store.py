"""Unit tests for VectorStore class"""
import pytest
import numpy as np
import tempfile
import shutil
from vector_store import VectorStore


class TestVectorStore:
    """Test suite for VectorStore"""

    def test_init_default_model(self):
        """Test initialization with default model"""
        store = VectorStore()
        assert store.embedding_model is not None
        assert store.index is None
        assert store.chunks is None
        assert store.dimension is None

    def test_init_custom_model(self):
        """Test initialization with custom model"""
        # Using the same model to avoid download times in tests
        store = VectorStore(model_name="sentence-transformers/all-MiniLM-L6-v2")
        assert store.embedding_model is not None

    def test_create_embeddings(self, sample_chunks):
        """Test creating embeddings for chunks"""
        store = VectorStore()
        embeddings = store.create_embeddings(sample_chunks)

        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape[0] == len(sample_chunks)
        assert embeddings.shape[1] > 0  # Has some dimension
        assert embeddings.dtype == np.float32 or embeddings.dtype == np.float64

    def test_create_embeddings_empty_list(self):
        """Test creating embeddings for empty chunk list"""
        store = VectorStore()
        embeddings = store.create_embeddings([])

        assert isinstance(embeddings, np.ndarray)
        assert embeddings.shape[0] == 0

    def test_build_index(self, sample_chunks):
        """Test building FAISS index"""
        store = VectorStore()
        store.build_index(sample_chunks)

        assert store.index is not None
        assert store.chunks == sample_chunks
        assert store.dimension > 0
        assert store.index.ntotal == len(sample_chunks)

    def test_search_basic(self, sample_chunks):
        """Test basic search functionality"""
        store = VectorStore()
        store.build_index(sample_chunks)

        query = "machine learning algorithms"
        results = store.search(query, top_k=2)

        assert isinstance(results, list)
        assert len(results) == 2
        assert all(isinstance(r, tuple) and len(r) == 2 for r in results)

        # Check structure
        for chunk, distance in results:
            assert 'text' in chunk
            assert isinstance(distance, float)
            assert distance >= 0

    def test_search_top_k(self, sample_chunks):
        """Test search with different top_k values"""
        store = VectorStore()
        store.build_index(sample_chunks)

        # Test various top_k values
        for k in [1, 2, 3]:
            results = store.search("test query", top_k=k)
            assert len(results) == k

    def test_search_without_index(self):
        """Test search raises error when index not built"""
        store = VectorStore()

        with pytest.raises(ValueError, match="Index not built"):
            store.search("test query")

    def test_search_relevance(self, sample_chunks):
        """Test that search returns relevant results"""
        store = VectorStore()
        store.build_index(sample_chunks)

        # Search for specific topic
        query = "machine learning"
        results = store.search(query, top_k=1)

        # The top result should be the most relevant
        top_chunk, _ = results[0]
        assert "machine learning" in top_chunk['text'].lower()

    def test_search_distance_ordering(self, sample_chunks):
        """Test that results are ordered by distance"""
        store = VectorStore()
        store.build_index(sample_chunks)

        results = store.search("neural networks", top_k=3)
        distances = [dist for _, dist in results]

        # Distances should be in ascending order
        assert distances == sorted(distances)

    def test_save_and_load(self, sample_chunks, tmp_path):
        """Test saving and loading vector store"""
        store = VectorStore()
        store.build_index(sample_chunks)

        # Save
        save_path = str(tmp_path / "vector_store")
        store.save(save_path)

        # Load into new store
        new_store = VectorStore()
        new_store.load(save_path)

        # Check that loaded store works
        assert new_store.index is not None
        assert new_store.chunks == sample_chunks
        assert new_store.dimension == store.dimension
        assert new_store.index.ntotal == store.index.ntotal

        # Test search on loaded store
        results = new_store.search("machine learning", top_k=1)
        assert len(results) == 1

    def test_save_creates_directory(self, sample_chunks, tmp_path):
        """Test that save creates directory if it doesn't exist"""
        store = VectorStore()
        store.build_index(sample_chunks)

        save_path = str(tmp_path / "new_dir" / "vector_store")
        store.save(save_path)

        # Check files exist
        import os
        assert os.path.exists(os.path.join(save_path, "index.faiss"))
        assert os.path.exists(os.path.join(save_path, "chunks.pkl"))

    def test_load_nonexistent_path(self):
        """Test loading from non-existent path raises error"""
        store = VectorStore()

        with pytest.raises(Exception):  # Could be FileNotFoundError or other
            store.load("/nonexistent/path")

    def test_embeddings_consistency(self, sample_chunks):
        """Test that same text produces same embeddings"""
        store = VectorStore()

        # Create embeddings twice
        embeddings1 = store.create_embeddings(sample_chunks)
        embeddings2 = store.create_embeddings(sample_chunks)

        # Should be identical
        np.testing.assert_array_almost_equal(embeddings1, embeddings2)

    def test_different_chunk_sizes(self):
        """Test index with different numbers of chunks"""
        store = VectorStore()

        for n_chunks in [1, 5, 10]:
            chunks = [
                {'id': i, 'text': f'Test chunk {i}', 'char_start': i*10, 'char_end': (i+1)*10}
                for i in range(n_chunks)
            ]
            store.build_index(chunks)
            assert store.index.ntotal == n_chunks

    def test_unicode_text(self):
        """Test handling of unicode text"""
        store = VectorStore()
        unicode_chunks = [
            {'id': 0, 'text': 'Hello world 你好世界', 'char_start': 0, 'char_end': 20},
            {'id': 1, 'text': 'Émojis and special chars: 🚀 ñ ü', 'char_start': 20, 'char_end': 50},
        ]

        store.build_index(unicode_chunks)
        results = store.search("hello", top_k=1)

        assert len(results) == 1
        assert results[0][0]['text'] == unicode_chunks[0]['text']
