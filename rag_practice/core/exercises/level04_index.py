"""Core 4: own an exact index and filter candidates before ranking."""

from ..types import Chunk, EmbedDocuments, EmbedQuery, SearchHit, VectorIndex


def build_index(chunks: list[Chunk], embed_documents: EmbedDocuments) -> VectorIndex:
    """Embed once and retain an independent immutable vector snapshot."""
    raise NotImplementedError("TODO CORE-4A: implement build_index")


def search_index(
    question: str,
    index: VectorIndex,
    embed_query: EmbedQuery,
    k: int = 5,
    allowed_sources: set[str] | None = None,
) -> list[SearchHit]:
    """Filter eligible sources, then perform exact cosine retrieval."""
    raise NotImplementedError("TODO CORE-4B: implement search_index")
