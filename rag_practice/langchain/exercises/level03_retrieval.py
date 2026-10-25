"""Level 3: index and retrieve documents without generation."""

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore


def build_index(
    chunks: list[Document], embeddings: Embeddings
) -> InMemoryVectorStore:
    """Build an independent in-memory index using the supplied embeddings."""
    raise NotImplementedError("TODO RAG-L3A: implement build_index")


def search_index(
    question: str, index: InMemoryVectorStore, k: int = 2
) -> list[Document]:
    """Return up to k matching chunks for a nonblank question."""
    raise NotImplementedError("TODO RAG-L3B: implement search_index")
