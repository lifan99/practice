"""Core 4: embedding ownership, filters before top-k, and failures."""

import pytest

from rag_practice.core.exercises.level04_index import build_index, search_index
from rag_practice.core.types import VectorIndex

pytestmark = pytest.mark.exercise


def test_index_embeds_once_and_snapshots_vectors(chunk):
    chunks = [chunk("a", "alpha"), chunk("b", "beta")]
    vectors = [[1.0, 0.0], [0.0, 1.0]]
    calls = []

    def embed(texts):
        calls.append(texts)
        return vectors

    index = build_index(chunks, embed)
    assert index.chunks == tuple(chunks)
    assert index.vectors == ((1.0, 0.0), (0.0, 1.0))
    assert calls == [["alpha", "beta"]]
    vectors[0][0] = 999
    chunks.clear()
    assert index.vectors[0][0] == 1.0
    assert len(index.chunks) == 2


@pytest.mark.parametrize("vectors", [[], [[1], [1]], [[]], [[float("nan")]]])
def test_invalid_embedding_result(chunk, vectors):
    with pytest.raises(ValueError):
        build_index([chunk()], lambda _: vectors)


def test_empty_and_duplicate_chunk_ids_fail_before_embedding(chunk):
    def forbidden(_):
        pytest.fail("Invalid chunks must not be embedded.")
    for chunks in ([], [chunk(), chunk()]):
        with pytest.raises(ValueError):
            build_index(chunks, forbidden)


def test_inconsistent_embedding_dimensions(chunk):
    with pytest.raises(ValueError):
        build_index([chunk("a"), chunk("b")], lambda _: [[1, 0], [1]])


def test_filter_applies_before_ranking_and_keeps_multiple_chunks_per_source(chunk):
    chunks = (chunk("secret", source="private.md"), chunk("a"), chunk("b"))
    index = VectorIndex(chunks, ((1, 0), (0.8, 0.6), (0, 1)))
    calls = []
    def query(text):
        calls.append(text)
        return [1, 0]
    hits = search_index("  question  ", index, query, 2, {"a.md"})
    assert [h.chunk.chunk_id for h in hits] == ["a", "b"]
    assert [h.score for h in hits] == pytest.approx([0.8, 0])
    assert calls == ["question"]


def test_no_eligible_sources_skips_embedding(chunk):
    def forbidden(_):
        pytest.fail("No eligible chunks means no query embedding.")
    index = VectorIndex((chunk(),), ((1, 0),))
    assert search_index("q", index, forbidden, allowed_sources=set()) == []
    assert search_index("q", index, forbidden, allowed_sources={"missing"}) == []


@pytest.mark.parametrize("question,k", [(" ", 1), ("q", 0)])
def test_invalid_query_before_callback(chunk, question, k):
    def forbidden(_):
        pytest.fail("Invalid query must not be embedded.")
    with pytest.raises(ValueError):
        search_index(question, VectorIndex((chunk(),), ((1,),)), forbidden, k)


def test_query_dimension_and_dependency_failures(chunk):
    index = VectorIndex((chunk(),), ((1, 0),))
    with pytest.raises(ValueError):
        search_index("q", index, lambda _: [1])
    def fail(_):
        raise OSError("offline")
    with pytest.raises(OSError, match="offline"):
        search_index("q", index, fail)
