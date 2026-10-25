"""Core 8: chunk-level fusion, stable score semantics, and composition."""

import pytest

from rag_practice.core import level08_hybrid as module

pytestmark = pytest.mark.exercise


def test_rrf_ignores_raw_score_scale_and_preserves_rank_positions(hit):
    rankings = [[hit("a", 1000), hit("a", 999), hit("b", 998)], [hit("b", -50), hit("c", -100)]]
    result = module.reciprocal_rank_fusion(rankings, 10, 0)
    assert [h.chunk.chunk_id for h in result] == ["b", "a", "c"]
    assert [h.score for h in result] == pytest.approx([1 + 1 / 3, 1, 0.5])
    assert result[0].chunk is rankings[0][2].chunk
    assert [len(r) for r in rankings] == [3, 2]


def test_ties_use_chunk_id_and_empty_lists_are_allowed(hit):
    assert [h.chunk.chunk_id for h in module.reciprocal_rank_fusion([[hit("z")], [hit("a")]], 2, 60)] == ["a", "z"]
    assert module.reciprocal_rank_fusion([[], []]) == []


@pytest.mark.parametrize("k,constant", [(0, 60), (1, -1)])
def test_invalid_fusion_configuration(k, constant):
    with pytest.raises(ValueError):
        module.reciprocal_rank_fusion([], k, constant)


def test_hybrid_calls_both_once_and_reuses_fusion(hit, monkeypatch):
    calls = []
    lexical_hits, dense_hits = [hit("lex")], [hit("dense")]
    def lexical(q):
        calls.append(("lexical", q))
        return lexical_hits
    def dense(q):
        calls.append(("dense", q))
        return dense_hits
    def fuse(rankings, k, rank_constant):
        assert rankings == [lexical_hits, dense_hits]
        assert (k, rank_constant) == (2, 5)
        return dense_hits
    monkeypatch.setattr(module, "reciprocal_rank_fusion", fuse)
    assert module.hybrid_search(" q ", lexical, dense, 2, 5) == dense_hits
    assert calls == [("lexical", "q"), ("dense", "q")]


def test_invalid_hybrid_before_retrieval():
    def forbidden(_):
        pytest.fail("Invalid input must not retrieve.")
    with pytest.raises(ValueError):
        module.hybrid_search(" ", forbidden, forbidden)
