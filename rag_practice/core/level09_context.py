"""Core 9: rerank and budget the fully rendered evidence context."""

from collections.abc import Callable

from .types import Chunk, SearchHit


def rerank(
    question: str, hits: list[SearchHit], score: Callable[[str, str], float], k: int = 5
) -> list[SearchHit]:
    """Score each unique chunk once and preserve candidate order on ties."""
    raise NotImplementedError("TODO CORE-9A: implement rerank")


def pack_context(
    chunks: list[Chunk], budget: int, count_tokens: Callable[[str], int]
) -> list[Chunk]:
    """Select whole chunks under the token count of the rendered context."""
    raise NotImplementedError("TODO CORE-9B: implement pack_context")
