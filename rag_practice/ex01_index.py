"""Compatibility imports; implement the exercises in levels 1 through 3."""

from .level01_documents import load_documents
from .level02_chunking import split_documents
from .level03_retrieval import build_index

__all__ = ["load_documents", "split_documents", "build_index"]
