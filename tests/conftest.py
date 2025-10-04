"""Pytest fixtures for RAG tests"""
import pytest
import tempfile
import os


@pytest.fixture
def sample_document():
    """Create a sample document for testing"""
    content = """# Test Document

This is the first paragraph of the test document.
It contains some sample text for testing purposes.

This is the second paragraph.
It also has multiple lines.
We use this to test chunking behavior.

This is the third paragraph.
It's a bit longer than the previous ones.
This helps us test the overlap functionality.
And we add more content to make it substantial.

Final paragraph here.
Testing complete."""
    return content


@pytest.fixture
def sample_document_file(tmp_path, sample_document):
    """Create a temporary file with sample document"""
    file_path = tmp_path / "test_doc.md"
    file_path.write_text(sample_document, encoding='utf-8')
    return str(file_path)


@pytest.fixture
def sample_chunks():
    """Sample chunks for vector store testing"""
    return [
        {'id': 0, 'text': 'This is the first chunk about machine learning', 'char_start': 0, 'char_end': 48},
        {'id': 1, 'text': 'This is the second chunk about deep learning', 'char_start': 48, 'char_end': 93},
        {'id': 2, 'text': 'This is the third chunk about neural networks', 'char_start': 93, 'char_end': 139},
    ]
