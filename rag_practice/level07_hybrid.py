"""Level 7: fuse lexical and vector retrieval rankings."""

from typing import TypedDict

from langchain_core.documents import Document
from langchain_core.runnables import Runnable


class RankedHit(TypedDict):
    chunk_id: str
    score: float


def reciprocal_rank_fusion(
    rankings: list[list[str]], rank_constant: int = 60, top_k: int = 5
) -> list[RankedHit]:
    """Fuse ranked chunk IDs using reciprocal rank fusion."""
    raise NotImplementedError("TODO RAG-L7A: implement reciprocal_rank_fusion")


def hybrid_search(
    question: str,
    lexical_retriever: Runnable,
    vector_retriever: Runnable,
    k: int = 5,
    rank_constant: int = 60,
) -> list[Document]:
    """Retrieve from two sources and return chunks in fused rank order."""
    raise NotImplementedError("TODO RAG-L7B: implement hybrid_search")
