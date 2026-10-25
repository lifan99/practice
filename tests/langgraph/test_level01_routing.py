"""Public behavior checks for this exercise level."""

from copy import deepcopy
import pytest
from langgraph.graph.state import CompiledStateGraph
from langgraph_practice.exercises.level01_routing import build_graph
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

