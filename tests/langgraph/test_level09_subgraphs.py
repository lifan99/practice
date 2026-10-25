"""Level 9: check compiled child graphs and explicit state mapping."""

from copy import deepcopy
from typing import TypedDict

import pytest
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from langgraph_practice.exercises.level09_subgraphs import build_normalizer_subgraph, build_report_graph

pytestmark = pytest.mark.exercise


def test_normalizer_subgraph():
    graph = build_normalizer_subgraph()
    assert isinstance(graph, CompiledStateGraph)
    initial = {"raw": "  one  two\nthree  "}
    result = graph.invoke(initial)
    assert result["clean"] == "one  two\nthree" and result["word_count"] == 3
    assert initial == {"raw": "  one  two\nthree  "}
    with pytest.raises(ValueError):
        graph.invoke({"raw": " \n"})


def fixture_child(transform):
    class ChildState(TypedDict, total=False):
        raw: str
        clean: str
        word_count: int

    builder = StateGraph(ChildState)
    builder.add_node("fixture", transform)
    builder.add_edge(START, "fixture")
    builder.add_edge("fixture", END)
    return builder.compile()


def test_parent_calls_supplied_child_and_keeps_private_keys_local():
    calls = []

    def transform(state):
        calls.append(state["raw"])
        return {"clean": state["raw"].strip(), "word_count": len(state["raw"].split())}

    graph = build_report_graph(fixture_child(transform))
    assert isinstance(graph, CompiledStateGraph)
    initial = {"document": "  one  two\n", "request_id": "req-1"}
    snapshot = deepcopy(initial)
    result = graph.invoke(initial)
    assert calls == ["  one  two\n"]
    assert result["text"] == "one  two" and result["word_count"] == 2
    assert result["report"] == "req-1: 2 words"
    assert result["document"] == initial["document"] and result["request_id"] == "req-1"
    assert "raw" not in result and "clean" not in result
    assert initial == snapshot


def test_child_failure_propagates():
    def fail(_):
        raise OSError("child unavailable")

    graph = build_report_graph(fixture_child(fail))
    with pytest.raises(OSError, match="child unavailable"):
        graph.invoke({"document": "input", "request_id": "req-1"})
