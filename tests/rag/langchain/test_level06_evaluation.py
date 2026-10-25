"""Level 6: check source recall and labeled query evaluation."""

from copy import deepcopy

import pytest
from langchain_core.documents import Document

pytestmark = pytest.mark.exercise

from langchain_core.runnables import RunnableLambda
from rag_practice.langchain.exercises.level06_evaluation import evaluate_retrieval, recall_at_k


@pytest.mark.parametrize("retrieved,relevant,k,expected", [
    (["a", "a", "b"], {"a", "b"}, 2, 0.5),
    (["a", "a", "b"], {"a", "b"}, 3, 1.0),
    (["x", "a"], {"a", "b"}, 1, 0.0),
    (["a"], {"a", "b"}, 10, 0.5),
    ([], {"a"}, 3, 0.0),
])
def test_source_recall(retrieved, relevant, k, expected):
    assert recall_at_k(retrieved, relevant, k) == pytest.approx(expected)



@pytest.mark.parametrize("relevant,k", [({"a"}, 0), ({"a"}, -1), (set(), 1)])
def test_invalid_recall_inputs(relevant, k):
    with pytest.raises(ValueError):
        recall_at_k([], relevant, k)


def test_evaluation_preserves_case_order_and_averages_per_question():
    cases = [
        {"question": "  first  ", "relevant_sources": {"a", "b"}},
        {"question": "second", "relevant_sources": {"b"}},
    ]
    snapshot = deepcopy(cases)
    queries = []

    def retrieve(question):
        queries.append(question)
        sources = ["a", "a", "b"] if question == "first" else ["b"]
        return [Document(page_content="evidence", metadata={"source": source}) for source in sources]

    report = evaluate_retrieval(cases, RunnableLambda(retrieve), k=2)
    assert report == {
        "mean_recall": 0.75,
        "per_query": [{"question": "first", "recall": 0.5}, {"question": "second", "recall": 1.0}],
    }
    assert queries == ["first", "second"]
    assert cases == snapshot


def test_evaluation_handles_empty_hits_and_repeated_questions():
    cases = [
        {"question": "same", "relevant_sources": {"a"}},
        {"question": "same", "relevant_sources": {"a", "b"}},
    ]
    calls = []

    def retrieve(question):
        calls.append(question)
        return []

    assert evaluate_retrieval(cases, RunnableLambda(retrieve), 1) == {
        "mean_recall": 0.0,
        "per_query": [{"question": "same", "recall": 0.0}, {"question": "same", "recall": 0.0}],
    }
    assert calls == ["same", "same"]


@pytest.mark.parametrize("cases,k", [
    ([], 1),
    ([{"question": "valid", "relevant_sources": {"a"}}], 0),
    ([{"question": "valid", "relevant_sources": {"a"}}], -1),
    ([{"question": "valid", "relevant_sources": {"a"}}, {"question": " ", "relevant_sources": {"b"}}], 1),
    ([{"question": "valid", "relevant_sources": {"a"}}, {"question": "bad", "relevant_sources": set()}], 1),
])
def test_evaluation_validates_all_cases_before_retrieval(cases, k):
    def forbidden(_):
        pytest.fail("All cases must be valid before the first retrieval.")

    with pytest.raises(ValueError):
        evaluate_retrieval(cases, RunnableLambda(forbidden), k)


def test_evaluation_propagates_retrieval_failure():
    def fail(_):
        raise OSError("retriever unavailable")

    with pytest.raises(OSError, match="retriever unavailable"):
        evaluate_retrieval([{"question": "q", "relevant_sources": {"a"}}], RunnableLambda(fail), 1)

