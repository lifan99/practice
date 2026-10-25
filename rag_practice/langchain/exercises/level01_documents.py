"""Level 1: represent local files as traceable documents."""

from pathlib import Path

from langchain_core.documents import Document


def load_documents(directory: Path) -> list[Document]:
    """Load nonempty UTF-8 Markdown files with source metadata."""
    raise NotImplementedError("TODO RAG-L1: implement load_documents")
