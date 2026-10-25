"""Level 7: check rank fusion and two-source retrieval."""

from copy import deepcopy

import pytest
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda

from rag_practice import level07_hybrid as hybrid

pytestmark = pytest.mark.exercise


def doc(chunk_id):
    return Document(page_content=f"Evidence {chunk_id}", metadata={"source": "same.md", "chunk_id": chunk_id})


def test_rrf_scores_and_order():
    rankings = [["a", "b"], ["b", "c"]]
    snapshot = deepcopy(rankings)
    hits = hybrid.reciprocal_rank_fusion(rankings, rank_constant=0)
    assert [hit["chunk_id"] for hit in hits] == ["b", "a", "c"]
    assert [hit["score"] for hit in hits] == pytest.approx([1.5, 1.0, 0.5])
    assert rankings == snapshot


def test_rrf_ties_and_top_k():
    hits = hybrid.reciprocal_rank_fusion([["b", "a"], ["a", "b"]], top_k=1)
    assert [hit["chunk_id"] for hit in hits] == ["a"]
    assert hits[0]["score"] == pytest.approx(1 / 61 + 1 / 62)


def test_rrf_duplicates_keep_original_rank_positions():
    hits = hybrid.reciprocal_rank_fusion([["a", "a", "b"]], rank_constant=0)
    assert [hit["chunk_id"] for hit in hits] == ["a", "b"]
    assert [hit["score"] for hit in hits] == pytest.approx([1.0, 1 / 3])


@pytest.mark.parametrize("rankings", [[], [[], []]])
def test_rrf_empty(rankings):
    assert hybrid.reciprocal_rank_fusion(rankings) == []


@pytest.mark.parametrize("constant,k", [(-1, 1), (0, 0), (60, -1)])
def test_rrf_invalid_parameters(constant, k):
    with pytest.raises(ValueError):
        hybrid.reciprocal_rank_fusion([], constant, k)


def test_hybrid_reuses_fusion_and_retains_first_document(monkeypatch):
    a, b, c = doc("a"), doc("b"), doc("c")
    lex_docs, vec_docs = [a, b], [deepcopy(b), c]
    snapshot = deepcopy((lex_docs, vec_docs))
    calls, fusions = [], []

    def lexical(question):
        calls.append(("lexical", question))
        return lex_docs

    def vector(question):
        calls.append(("vector", question))
        return vec_docs

    def fuse(rankings, rank_constant=60, top_k=5):
        fusions.append((rankings, rank_constant, top_k))
        return [{"chunk_id": "b", "score": 2.0}, {"chunk_id": "a", "score": 1.0}]

    monkeypatch.setattr(hybrid, "reciprocal_rank_fusion", fuse)
    result = hybrid.hybrid_search("  query  ", RunnableLambda(lexical), RunnableLambda(vector), 2, 30)
    assert sorted(calls) == [("lexical", "query"), ("vector", "query")]
    assert fusions == [([["a", "b"], ["b", "c"]], 30, 2)]
    assert result == [b, a]
    assert result[0] is b
    assert (lex_docs, vec_docs) == snapshot


@pytest.mark.parametrize("lexical,vector,expected", [([], ["b"], ["b"]), (["a"], [], ["a"]), ([], [], [])])
def test_hybrid_empty_branches(lexical, vector, expected):
    result = hybrid.hybrid_search("query", RunnableLambda(lambda _: [doc(x) for x in lexical]), RunnableLambda(lambda _: [doc(x) for x in vector]))
    assert [hit.metadata["chunk_id"] for hit in result] == expected


@pytest.mark.parametrize("question,k,constant", [(" ", 1, 60), ("q", 0, 60), ("q", 1, -1)])
def test_hybrid_validates_before_dependencies(question, k, constant):
    def forbidden(_):
        pytest.fail("Invalid input must not retrieve.")

    with pytest.raises(ValueError):
        hybrid.hybrid_search(question, RunnableLambda(forbidden), RunnableLambda(forbidden), k, constant)
