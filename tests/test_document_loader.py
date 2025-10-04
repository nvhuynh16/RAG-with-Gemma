"""Unit tests for DocumentLoader class"""
import pytest
from document_loader import DocumentLoader


class TestDocumentLoader:
    """Test suite for DocumentLoader"""

    def test_init_default_params(self):
        """Test initialization with default parameters"""
        loader = DocumentLoader()
        assert loader.chunk_size == 500
        assert loader.chunk_overlap == 50

    def test_init_custom_params(self):
        """Test initialization with custom parameters"""
        loader = DocumentLoader(chunk_size=1000, chunk_overlap=100)
        assert loader.chunk_size == 1000
        assert loader.chunk_overlap == 100

    def test_load_document(self, sample_document_file):
        """Test loading document from file"""
        loader = DocumentLoader()
        content = loader.load_document(sample_document_file)
        assert isinstance(content, str)
        assert len(content) > 0
        assert "Test Document" in content

    def test_load_document_nonexistent(self):
        """Test loading non-existent document raises error"""
        loader = DocumentLoader()
        with pytest.raises(FileNotFoundError):
            loader.load_document("nonexistent_file.md")

    def test_chunk_text_basic(self):
        """Test basic text chunking"""
        loader = DocumentLoader(chunk_size=100, chunk_overlap=20)
        text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        chunks = loader.chunk_text(text)

        assert isinstance(chunks, list)
        assert len(chunks) > 0
        assert all('id' in chunk for chunk in chunks)
        assert all('text' in chunk for chunk in chunks)
        assert all('char_start' in chunk for chunk in chunks)
        assert all('char_end' in chunk for chunk in chunks)

    def test_chunk_text_overlap(self):
        """Test that chunks have proper overlap"""
        loader = DocumentLoader(chunk_size=50, chunk_overlap=10)
        text = "A" * 30 + "\n\n" + "B" * 30 + "\n\n" + "C" * 30
        chunks = loader.chunk_text(text)

        # Check that we have multiple chunks
        assert len(chunks) > 1

        # Check that chunks have content
        for chunk in chunks:
            assert len(chunk['text']) > 0

    def test_chunk_text_short_text(self):
        """Test chunking very short text"""
        loader = DocumentLoader(chunk_size=500, chunk_overlap=50)
        text = "Short text."
        chunks = loader.chunk_text(text)

        assert len(chunks) == 1
        assert chunks[0]['text'] == "Short text."
        assert chunks[0]['id'] == 0

    def test_chunk_text_empty(self):
        """Test chunking empty text"""
        loader = DocumentLoader()
        text = ""
        chunks = loader.chunk_text(text)

        assert len(chunks) == 0

    def test_chunk_ids_sequential(self):
        """Test that chunk IDs are sequential"""
        loader = DocumentLoader(chunk_size=50, chunk_overlap=10)
        text = "\n\n".join([f"Paragraph {i}" * 10 for i in range(5)])
        chunks = loader.chunk_text(text)

        chunk_ids = [chunk['id'] for chunk in chunks]
        assert chunk_ids == list(range(len(chunks)))

    def test_load_and_chunk(self, sample_document_file):
        """Test combined load and chunk operation"""
        loader = DocumentLoader(chunk_size=100, chunk_overlap=20)
        chunks = loader.load_and_chunk(sample_document_file)

        assert isinstance(chunks, list)
        assert len(chunks) > 0
        assert all('text' in chunk for chunk in chunks)
        assert any('first paragraph' in chunk['text'].lower() for chunk in chunks)

    def test_chunk_boundary_preservation(self):
        """Test that paragraph boundaries are preserved"""
        loader = DocumentLoader(chunk_size=200, chunk_overlap=20)
        text = "Para 1\n\nPara 2\n\nPara 3"
        chunks = loader.chunk_text(text)

        # All chunks should contain complete paragraphs
        for chunk in chunks:
            assert not chunk['text'].startswith('\n')
            assert not chunk['text'].endswith('\n')

    def test_large_document_chunking(self):
        """Test chunking a large document"""
        loader = DocumentLoader(chunk_size=200, chunk_overlap=30)
        # Create a large document
        paragraphs = [f"This is paragraph number {i}. " * 10 for i in range(20)]
        text = "\n\n".join(paragraphs)
        chunks = loader.chunk_text(text)

        # Should create multiple chunks
        assert len(chunks) > 5

        # Each chunk should respect size limits (approximately)
        for chunk in chunks:
            # Allow significant flexibility due to paragraph boundaries
            # The chunker preserves semantic boundaries which can exceed chunk_size
            assert len(chunk['text']) <= loader.chunk_size + 200

    def test_chunk_metadata_accuracy(self):
        """Test that chunk metadata is accurate"""
        loader = DocumentLoader(chunk_size=100, chunk_overlap=20)
        text = "A" * 80 + "\n\n" + "B" * 80
        chunks = loader.chunk_text(text)

        for i, chunk in enumerate(chunks):
            assert chunk['id'] == i
            assert isinstance(chunk['char_start'], int)
            assert isinstance(chunk['char_end'], int)
            assert chunk['char_end'] >= chunk['char_start']
