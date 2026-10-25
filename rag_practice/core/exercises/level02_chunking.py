"""Core 2: implement overlapping windows and paragraph-aware chunks."""

from ..types import Chunk, Document


def window_chunks(document: Document, size: int, overlap: int = 0) -> list[Chunk]:
    """Create windows retaining exact source offsets and stable IDs."""
    raise NotImplementedError("TODO CORE-2A: implement window_chunks")


def paragraph_chunks(document: Document, max_chars: int) -> list[Chunk]:
    """Pack complete paragraphs and split oversized paragraphs."""
    raise NotImplementedError("TODO CORE-2B: implement paragraph_chunks")
