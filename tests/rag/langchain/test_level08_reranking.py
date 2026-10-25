"""Level 8: check reranking and complete-chunk context budgets."""

from copy import deepcopy

import pytest
from langchain_core.documents import Document

from rag_practice.langchain.exercises.level08_reranking import pack_context, rerank

pytestmark = pytest.mark.exercise


def doc(chunk_id, content):
    return Document(page_content=content, metadata={"source": "same.md", "chunk_id": chunk_id})


def test_reranking_deduplicates_scores_once_and_preserves_ties():
    docs = [doc("a", "alpha"), doc("b", "beta"), doc("c", "gamma"), doc("a", "alpha")]
    snapshot = deepcopy(docs)
    calls = []

    def scorer(question, content):
        calls.append((question, content))
        return {"alpha": -1.0, "beta": 5.0, "gamma": 5.0}[content]

    result = rerank("  query  ", docs, scorer, 2)
    assert [hit.metadata["chunk_id"] for hit in result] == ["b", "c"]
    assert calls == [("query", "alpha"), ("query", "beta"), ("query", "gamma")]
    assert docs == snapshot


def test_reranking_empty_input():
    def forbidden(*args):
        pytest.fail("Empty input must not score.")

    assert rerank("query", [], forbidden) == []


@pytest.mark.parametrize("question,k", [(" ", 1), ("q", 0), ("q", -1)])
def test_reranking_validates_before_scoring(question, k):
    def forbidden(*args):
        pytest.fail("Invalid input must not score.")

    with pytest.raises(ValueError):
        rerank(question, [], forbidden, k)


@pytest.mark.parametrize("score", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_scores_rejected(score):
    with pytest.raises(ValueError):
        rerank("query", [doc("a", "alpha")], lambda *_: score)


def test_scorer_error_propagates():
    def fail(*args):
        raise OSError("scorer unavailable")

    with pytest.raises(OSError, match="scorer unavailable"):
        rerank("query", [doc("a", "alpha")], fail)


def test_budget_skips_long_chunks_and_keeps_later_fits():
    docs = [doc("a", "a" * 8), doc("b", "b" * 20), doc("c", "中文")]
    snapshot = deepcopy(docs)
    assert pack_context(docs, 10) == [docs[0], docs[2]]
    assert docs == snapshot


@pytest.mark.parametrize("documents,budget,expected", [
    ([], 1, []),
    ([doc("a", "abcd")], 3, []),
    ([doc("a", "abcd")], 4, [doc("a", "abcd")]),
])
def test_budget_edges(documents, budget, expected):
    assert pack_context(documents, budget) == expected


@pytest.mark.parametrize("budget", [0, -1])
def test_invalid_budget(budget):
    with pytest.raises(ValueError):
        pack_context([], budget)
