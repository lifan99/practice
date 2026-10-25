"""Public behavior checks for branching and bounded retries."""

from copy import deepcopy

import pytest
from langgraph.graph.state import CompiledStateGraph

from langgraph_practice.ex01_routing import build_graph
from langgraph_practice.ex02_retry import build_retry_graph

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("question,category", [
    ("  REFUND please  ", "billing"),
    ("how do refunds work?", "billing"),
    ("How do I sign in?", "general"),
])
def test_routing(question, category):
    graph = build_graph()
    assert isinstance(graph, CompiledStateGraph)
    initial = {"question": question}
    snapshot = deepcopy(initial)
    result = graph.invoke(initial)
    assert result["question"] == question.strip()
    assert result["category"] == category
    assert result["answer"] == f"Contact {category} support."
    assert result["trace"] == ["normalize", "classify", category]
    assert initial == snapshot


def test_empty_question_is_invalid():
    graph = build_graph()
    with pytest.raises(ValueError):
        graph.invoke({"question": " \n\t "})


def test_routing_graph_has_no_state_leak():
    graph = build_graph()
    graph.invoke({"question": "refund"})
    result = graph.invoke({"question": "login"})
    assert result["trace"] == ["normalize", "classify", "general"]


@pytest.mark.parametrize("succeed_at,limit,attempts,done,status", [
    (1, 3, 1, True, "success"),
    (2, 3, 2, True, "success"),
    (3, 3, 3, True, "success"),
    (99, 3, 3, False, "exhausted"),
    (99, 1, 1, False, "exhausted"),
])
def test_retry_boundaries(succeed_at, limit, attempts, done, status):
    calls = []

    def checker(attempt):
        calls.append(attempt)
        return attempt == succeed_at

    graph = build_retry_graph(checker, max_attempts=limit)
    assert isinstance(graph, CompiledStateGraph)
    result = graph.invoke({"attempts": 0, "done": False})
    assert result["attempts"] == attempts
    assert result["done"] is done
    assert result["status"] == status
    assert calls == list(range(1, attempts + 1))


@pytest.mark.parametrize("limit", [0, -1])
def test_invalid_attempt_limit(limit):
    with pytest.raises(ValueError):
        build_retry_graph(lambda _: False, max_attempts=limit)


def test_retry_graph_reusable():
    calls = []

    def checker(attempt):
        calls.append(attempt)
        return attempt == 2

    graph = build_retry_graph(checker)
    for _ in range(2):
        assert graph.invoke({"attempts": 0, "done": False})["attempts"] == 2
    assert calls == [1, 2, 1, 2]


def test_checker_exception_propagates():
    def checker(_):
        raise RuntimeError("checker unavailable")

    graph = build_retry_graph(checker)
    with pytest.raises(RuntimeError, match="checker unavailable"):
        graph.invoke({"attempts": 0, "done": False})
