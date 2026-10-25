"""Core 5: BM25 statistics and explicitly chosen score convention."""

import math

import pytest

from rag_practice.core.level05_bm25 import build_bm25, search_bm25
from rag_practice.core.types import BM25Index

pytestmark = pytest.mark.exercise


def test_build_preserves_repeated_tokens_and_captures_snapshot(chunk):
    chunks = [chunk("a", "cat cat"), chunk("b", "dog")]
    outputs = []
    def tokenize(text):
        result = text.split()
        outputs.append(result)
        return result
    index = build_bm25(chunks, tokenize, 1.2, 0.5)
    assert index.tokens == (("cat", "cat"), ("dog",))
    assert (index.k1, index.b) == (1.2, 0.5)
    outputs[0].clear()
    chunks.clear()
    assert len(index.chunks) == 2 and index.tokens[0] == ("cat", "cat")


def test_known_scores_document_frequency_and_query_deduplication(chunk):
    chunks = (chunk("a"), chunk("b"), chunk("c"))
    index = BM25Index(chunks, (("cat", "cat"), ("cat", "dog"), ("dog",)), 1.5, 0.75)
    hits = search_bm25("cat cat", index, str.split, 10)
    assert [h.chunk.chunk_id for h in hits] == ["a", "b"]
    idf = math.log(1 + 1.5 / 2.5)
    assert [h.score for h in hits] == pytest.approx([
        idf * 5 / (2 + 1.5 * (0.25 + 0.75 * 2 / (5 / 3))),
        idf * 2.5 / (1 + 1.5 * (0.25 + 0.75 * 2 / (5 / 3))),
    ])


def test_no_matching_terms_or_empty_tokenized_corpus(chunk):
    index = BM25Index((chunk(),), ((),))
    assert search_bm25("word", index, str.split) == []
    assert search_bm25("punctuation", index, lambda _: []) == []
    nonempty = BM25Index((chunk(),), (("known",),))
    assert search_bm25("unknown", nonempty, str.split) == []


def test_ties_preserve_corpus_order_and_b_zero_disables_length_effect(chunk):
    index = BM25Index((chunk("b"), chunk("a")), (("cat", "dog"), ("cat",)), 1.5, 0)
    hits = search_bm25("cat", index, str.split)
    assert [h.chunk.chunk_id for h in hits] == ["b", "a"]
    assert hits[0].score == pytest.approx(hits[1].score)


@pytest.mark.parametrize("k1,b", [(0, 0.5), (-1, 0.5), (1, -0.1), (1, 1.1), (float("nan"), 0), (1, float("inf"))])
def test_invalid_parameters_before_tokenization(chunk, k1, b):
    def forbidden(_):
        pytest.fail("Invalid config must not tokenize.")
    with pytest.raises(ValueError):
        build_bm25([chunk()], forbidden, k1, b)


def test_empty_or_duplicate_corpus_before_tokenization(chunk):
    def forbidden(_):
        pytest.fail("Invalid corpus must not tokenize.")
    for chunks in ([], [chunk(), chunk()]):
        with pytest.raises(ValueError):
            build_bm25(chunks, forbidden)


@pytest.mark.parametrize("question,k", [(" ", 1), ("q", 0)])
def test_invalid_search(chunk, question, k):
    def forbidden(_):
        pytest.fail("Invalid query must not tokenize.")
    with pytest.raises(ValueError):
        search_bm25(question, BM25Index((chunk(),), (("q",),)), forbidden, k)
