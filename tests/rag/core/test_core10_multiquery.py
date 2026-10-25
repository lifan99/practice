"""Core 10: original query retention, expansion limits, and fusion reuse."""

import pytest

from rag_practice.core import level08_hybrid
from rag_practice.core.level10_multiquery import multi_query_search

pytestmark = pytest.mark.exercise


def test_normalizes_deduplicates_bounds_and_fuses(hit, monkeypatch):
    queries, rewrites = [], []
    def rewrite(q):
        rewrites.append(q)
        return [" q ", " ", " alternate ", "alternate", "third", "fourth"]
    def retrieve(q):
        queries.append(q)
        return [hit(q)]
    def fuse(rankings, k, rank_constant):
        assert [r[0].chunk.chunk_id for r in rankings] == ["q", "alternate", "third"]
        assert (k, rank_constant) == (2, 7)
        return rankings[0]
    monkeypatch.setattr(level08_hybrid, "reciprocal_rank_fusion", fuse)
    assert multi_query_search(" q ", rewrite, retrieve, 3, 2, 7)[0].chunk.chunk_id == "q"
    assert queries == ["q", "alternate", "third"] and rewrites == ["q"]


def test_single_query_does_not_rewrite(hit, monkeypatch):
    def forbidden(_):
        pytest.fail("A one-query budget must not rewrite.")
    monkeypatch.setattr(level08_hybrid, "reciprocal_rank_fusion", lambda rankings, k, rank_constant: rankings[0])
    assert multi_query_search("q", forbidden, lambda _: [hit()], 1)[0].chunk.chunk_id == "a"


@pytest.mark.parametrize("question,max_queries,k,constant", [(" ", 1, 1, 0), ("q", 0, 1, 0), ("q", 1, 0, 0), ("q", 1, 1, -1)])
def test_invalid_request_before_dependencies(question, max_queries, k, constant):
    def forbidden(_):
        pytest.fail("Invalid request must not call dependencies.")
    with pytest.raises(ValueError):
        multi_query_search(question, forbidden, forbidden, max_queries, k, constant)


def test_empty_expansion_still_retrieves_original(monkeypatch):
    queries = []
    monkeypatch.setattr(level08_hybrid, "reciprocal_rank_fusion", lambda rankings, k, rank_constant: [])
    def retrieve(q):
        queries.append(q)
        return []
    assert multi_query_search("q", lambda _: [], retrieve) == []
    assert queries == ["q"]


def test_dependency_error_propagates():
    def fail(_):
        raise OSError("rewrite unavailable")
    with pytest.raises(OSError, match="rewrite unavailable"):
        multi_query_search("q", fail, lambda _: [])
