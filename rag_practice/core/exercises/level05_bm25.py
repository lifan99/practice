"""Core 5: implement lexical retrieval from corpus statistics."""

from ..types import BM25Index, Chunk, SearchHit, Tokenizer


def build_bm25(
    chunks: list[Chunk], tokenize: Tokenizer, k1: float = 1.5, b: float = 0.75
) -> BM25Index:
    """Capture chunk tokens and validate BM25 configuration."""
    raise NotImplementedError("TODO CORE-5A: implement build_bm25")


def search_bm25(
    question: str, index: BM25Index, tokenize: Tokenizer, k: int = 5
) -> list[SearchHit]:
    """Compute the specified BM25 variant and return positive-score hits."""
    raise NotImplementedError("TODO CORE-5B: implement search_bm25")
