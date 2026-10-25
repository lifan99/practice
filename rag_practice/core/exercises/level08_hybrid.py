"""Core 8: fuse actual lexical and vector retrievers by rank."""

from ..types import Retriever, SearchHit


def reciprocal_rank_fusion(
    rankings: list[list[SearchHit]], k: int = 5, rank_constant: int = 60
) -> list[SearchHit]:
    """Fuse by chunk ID without mixing incomparable raw score scales."""
    raise NotImplementedError("TODO CORE-8A: implement reciprocal_rank_fusion")


def hybrid_search(
    question: str, lexical: Retriever, dense: Retriever, k: int = 5, rank_constant: int = 60
) -> list[SearchHit]:
    """Call both retrievers and rank their combined candidates."""
    raise NotImplementedError("TODO CORE-8B: implement hybrid_search")
