"""Core 3: compute cosine scores and exact top-k retrieval."""

from ..types import Vector


def cosine_similarity(left: Vector, right: Vector) -> float:
    """Score finite vectors, defining a zero-vector cosine as zero."""
    raise NotImplementedError("TODO CORE-3A: implement cosine_similarity")


def top_k_vectors(query: Vector, vectors: list[Vector], k: int) -> list[tuple[int, float]]:
    """Return row positions and scores with stable input-order ties."""
    raise NotImplementedError("TODO CORE-3B: implement top_k_vectors")
