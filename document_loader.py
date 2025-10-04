"""
Document Loader and Chunking Module
Loads and chunks documents for RAG pipeline
"""
from typing import List, Dict, Any


class DocumentLoader:
    """Load and process markdown documents"""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize document loader

        Args:
            chunk_size: Maximum number of characters per chunk
            chunk_overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_document(self, file_path: str) -> str:
        """
        Load document from file

        Args:
            file_path: Path to the document

        Returns:
            Document content as string
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks

        Args:
            text: Input text to chunk

        Returns:
            List of chunks with metadata
        """
        chunks = []
        start = 0
        chunk_id = 0

        # Split by paragraphs first for better semantic boundaries
        paragraphs = text.split('\n\n')
        current_chunk = ""

        for para in paragraphs:
            # If adding this paragraph exceeds chunk size, save current chunk
            if len(current_chunk) + len(para) > self.chunk_size and current_chunk:
                chunks.append({
                    'id': chunk_id,
                    'text': current_chunk.strip(),
                    'char_start': start,
                    'char_end': start + len(current_chunk)
                })

                # Create overlap
                overlap_start = max(0, len(current_chunk) - self.chunk_overlap)
                current_chunk = current_chunk[overlap_start:] + "\n\n" + para
                start += overlap_start
                chunk_id += 1
            else:
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para

        # Add the last chunk
        if current_chunk:
            chunks.append({
                'id': chunk_id,
                'text': current_chunk.strip(),
                'char_start': start,
                'char_end': start + len(current_chunk)
            })

        return chunks

    def load_and_chunk(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load document and split into chunks

        Args:
            file_path: Path to the document

        Returns:
            List of chunks with metadata
        """
        content = self.load_document(file_path)
        chunks = self.chunk_text(content)
        return chunks


if __name__ == "__main__":
    # Test the document loader
    loader = DocumentLoader(chunk_size=500, chunk_overlap=50)
    chunks = loader.load_and_chunk("radar-calibration-doc.md")

    print(f"Loaded {len(chunks)} chunks from document")
    print(f"\nFirst chunk preview:")
    print(chunks[0]['text'][:200] + "...")
