"""Exercise 1: load documents, split text, and build an index."""

from pathlib import Path

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore


def load_documents(directory: Path) -> list[Document]:
    """Load nonempty UTF-8 Markdown files with source metadata."""
    raise NotImplementedError("TODO RAG-1A: implement load_documents")


def split_documents(
    documents: list[Document], chunk_size: int = 160, chunk_overlap: int = 30
) -> list[Document]:
    """Split documents while retaining source metadata."""
    raise NotImplementedError("TODO RAG-1B: implement split_documents")


def build_index(
    chunks: list[Document], embeddings: Embeddings
) -> InMemoryVectorStore:
    """Build an in-memory index with the supplied embedding model."""
    raise NotImplementedError("TODO RAG-1C: implement build_index")
