"""Level 2: compare fixed character windows with recursive splitting."""

from langchain_core.documents import Document


def fixed_size_chunks(text: str, chunk_size: int, chunk_overlap: int = 0) -> list[str]:
    """Split text into overlapping character windows without losing content."""
    raise NotImplementedError("TODO RAG-L2A: implement fixed_size_chunks")


def split_documents(
    documents: list[Document], chunk_size: int = 160, chunk_overlap: int = 30
) -> list[Document]:
    """Recursively split documents while retaining their metadata."""
    raise NotImplementedError("TODO RAG-L2B: implement split_documents")
