"""Core 9: unique reranking and full-render token accounting."""

import pytest

from rag_practice.core import level09_context as module
from rag_practice.core import level06_pipeline

pytestmark = pytest.mark.exercise


def test_rerank_scores_unique_chunks_once_and_preserves_ties(hit):
    hits = [hit("a", 500, "alpha"), hit("b", 1, "beta"), hit("a", 100, "alpha"), hit("c", 0, "gamma")]
    calls = []
    def score(question, text):
        calls.append((question, text))
        return {"alpha": -1, "beta": 2, "gamma": 2}[text]
    result = module.rerank(" q ", hits, score, 2)
    assert [h.chunk.chunk_id for h in result] == ["b", "c"]
    assert [h.score for h in result] == [2, 2]
    assert calls == [("q", "alpha"), ("q", "beta"), ("q", "gamma")]
    assert hits[0].score == 500


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_invalid_rerank_score(hit, value):
    with pytest.raises(ValueError):
        module.rerank("q", [hit()], lambda *_: value)


def test_rerank_validates_before_scoring():
    def forbidden(*_):
        pytest.fail("Invalid request must not score.")
    with pytest.raises(ValueError):
        module.rerank(" ", [], forbidden)
    with pytest.raises(ValueError):
        module.rerank("q", [], forbidden, 0)
    assert module.rerank("q", [], forbidden) == []


def test_budget_counts_headers_and_separators_skips_long_chunk(chunk, monkeypatch):
    chunks = [chunk("a", "x"), chunk("b", "b" * 30), chunk("c", "z")]
    rendered = []
    def render(selected):
        return "|".join(f"HEADER:{c.chunk_id}:{c.text}" for c in selected)
    monkeypatch.setattr(level06_pipeline, "format_context", render)
    # The packing module must reuse this function, not duplicate its formatting.
    def count_tokens(text):
        rendered.append(text)
        return len(text)
    result = module.pack_context(chunks, len(render([chunks[0], chunks[2]])), count_tokens)
    assert result == [chunks[0], chunks[2]]
    assert render([chunks[0], chunks[1]]) in rendered
    assert render([chunks[0], chunks[2]]) in rendered


def test_token_counter_is_injected_not_assumed_to_be_character_length(chunk, monkeypatch):
    monkeypatch.setattr(level06_pipeline, "format_context", lambda selected: " ".join(c.text for c in selected))
    chunks = [chunk("a", "longword"), chunk("b", "two words"), chunk("c", "last")]
    assert module.pack_context(chunks, 2, lambda text: len(text.split())) == [chunks[0], chunks[2]]
    assert module.pack_context([], 1, lambda _: 0) == []


@pytest.mark.parametrize("budget,count", [(0, 1), (1, -1), (1, 1.5)])
def test_invalid_budget_or_token_count(chunk, monkeypatch, budget, count):
    monkeypatch.setattr(level06_pipeline, "format_context", lambda _: "context")
    with pytest.raises(ValueError):
        module.pack_context([chunk()], budget, lambda _: count)
