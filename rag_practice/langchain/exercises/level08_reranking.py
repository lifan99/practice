"""Level 8: rerank candidates and select a bounded evidence context."""

from collections.abc import Callable

from langchain_core.documents import Document


def rerank(
    question: str,
    documents: list[Document],
    scorer: Callable[[str, str], float],
    top_k: int = 3,
) -> list[Document]:
    """Score unique chunks and return the highest-scoring candidates."""
    raise NotImplementedError("TODO RAG-L8A: implement rerank")


def pack_context(documents: list[Document], max_chars: int) -> list[Document]:
    """Select whole chunks in rank order within a content-character budget."""
    raise NotImplementedError("TODO RAG-L8B: implement pack_context")
