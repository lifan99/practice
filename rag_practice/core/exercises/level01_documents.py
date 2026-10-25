"""Core 1: load source-preserving documents without a framework."""

from pathlib import Path

from ..types import Document


def load_documents(directory: Path) -> list[Document]:
    """Load nonblank UTF-8 Markdown files in filename order."""
    raise NotImplementedError("TODO CORE-1: implement load_documents")
