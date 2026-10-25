"""Core 7: rank-sensitive metrics, duplicates, graded labels, and macro means."""

import math
from copy import deepcopy

import pytest

from rag_practice.core import level07_metrics as module

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("ranked,relevant,k,recall,rr", [
    (["a", "a", "b"], {"a", "b"}, 2, 0.5, 1.0),
    (["x", "b", "a"], {"a", "b"}, 3, 1.0, 0.5),
    (["x"], {"a"}, 10, 0.0, 0.0),
    ([], {"a"}, 1, 0.0, 0.0),
    (["a"], set(), 1, 0.0, 0.0),
])
def test_binary_metrics(ranked, relevant, k, recall, rr):
    assert module.recall_at_k(ranked, relevant, k) == pytest.approx(recall)
    assert module.reciprocal_rank_at_k(ranked, relevant, k) == pytest.approx(rr)


def test_ndcg_uses_exponential_gain_and_does_not_reward_repeated_ids():
    labels = {"a": 3, "b": 1, "c": 0}
    ideal = 7 + 1 / math.log2(3)
    assert module.ndcg_at_k(["b", "a"], labels, 2) == pytest.approx((1 + 7 / math.log2(3)) / ideal)
    assert module.ndcg_at_k(["a", "a", "b"], labels, 3) == pytest.approx((7 + 1 / 2) / ideal)
    assert module.ndcg_at_k(["a", "b"], labels, 2) == pytest.approx(1)
    assert module.ndcg_at_k(["unknown"], labels, 1) == 0


@pytest.mark.parametrize("labels", [{}, {"a": 0}])
def test_zero_ideal_gain(labels):
    assert module.ndcg_at_k(["a"], labels, 3) == 0.0


def test_invalid_k_and_negative_grade():
    for function, labels in ((module.recall_at_k, {"a"}), (module.reciprocal_rank_at_k, {"a"}), (module.ndcg_at_k, {"a": 1})):
        with pytest.raises(ValueError):
            function([], labels, 0)
    with pytest.raises(ValueError):
        module.ndcg_at_k([], {"a": -1}, 1)


@pytest.mark.parametrize("grade", [4, 1.5, True])
def test_invalid_relevance_grade(grade):
    with pytest.raises(ValueError):
        module.ndcg_at_k([], {"a": grade}, 1)


def test_evaluation_averages_per_query_and_preserves_input(hit):
    cases = [{"question": "  first  ", "relevance": {"a": 1, "b": 1}}, {"question": "none", "relevance": {}}]
    before = deepcopy(cases)
    calls = []
    def retrieve(question):
        calls.append(question)
        return [hit("a")] if question == "first" else []
    report = module.evaluate(cases, retrieve, 2)
    assert report == pytest.approx({
        "recall": 0.25, "mrr": 0.5, "ndcg": 0.5 / (1 + 1 / math.log2(3))
    })
    assert calls == ["first", "none"] and cases == before


@pytest.mark.parametrize("cases,k", [
    ([], 1), ([{"question": "q", "relevance": {}}], 0),
    ([{"question": "q", "relevance": {}}, {"question": " ", "relevance": {}}], 1),
    ([{"question": "q", "relevance": {}}, {"question": "x", "relevance": {"a": -1}}], 1),
])
def test_validate_entire_dataset_before_first_query(cases, k):
    def forbidden(_):
        pytest.fail("Validate the whole dataset first.")
    with pytest.raises(ValueError):
        module.evaluate(cases, forbidden, k)
