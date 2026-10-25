"""Small independent inputs for the handwritten RAG track."""

import pytest

from rag_practice.core.types import Chunk, SearchHit


@pytest.fixture
def chunk():
    def make(chunk_id="a", text="evidence", source="a.md", start=0):
        return Chunk(chunk_id, text, source, start, start + len(text))
    return make


@pytest.fixture
def hit(chunk):
    def make(chunk_id="a", score=1.0, text="evidence", source="a.md"):
        return SearchHit(chunk(chunk_id, text, source), score)
    return make
