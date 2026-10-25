"""Core 10: bound expanded queries and merge their retrieval candidates."""

from collections.abc import Callable

from ..types import Retriever, SearchHit


def multi_query_search(
    question: str,
    rewrite: Callable[[str], list[str]],
    retrieve: Retriever,
    max_queries: int = 3,
    k: int = 5,
    rank_constant: int = 60,
) -> list[SearchHit]:
    """Keep the original query, deduplicate expansions, and fuse rankings."""
    raise NotImplementedError("TODO CORE-10: implement multi_query_search")
