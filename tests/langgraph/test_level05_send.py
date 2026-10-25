"""Level 5: check dynamically dispatched occurrences and input order."""

from collections import Counter
from copy import deepcopy

import pytest
from langgraph.graph.state import CompiledStateGraph

from langgraph_practice.exercises.level05_send import build_map_graph

pytestmark = pytest.mark.exercise


def test_dynamic_workers_preserve_duplicate_positions():
    calls = []

    def worker(value):
        calls.append(value)
        return value * value

    graph = build_map_graph(worker)
    assert isinstance(graph, CompiledStateGraph)
    initial = {"items": [3, 1, 3, -2]}
    snapshot = deepcopy(initial)
    result = graph.invoke(initial)
    assert result["results"] == [9, 1, 9, 4]
    assert sorted(result["mapped"], key=lambda item: item["index"]) == [{"index": 0, "value": 9}, {"index": 1, "value": 1}, {"index": 2, "value": 9}, {"index": 3, "value": 4}]
    assert Counter(calls) == Counter(initial["items"])
    assert initial == snapshot


def test_empty_map_and_repeat_invocation():
    graph = build_map_graph(lambda value: value + 1)
    graph.invoke({"items": [1, 2]})
    result = graph.invoke({"items": []})
    assert result["results"] == [] and result["mapped"] == []


def test_worker_failure_propagates():
    def fail(_):
        raise OSError("worker unavailable")

    graph = build_map_graph(fail)
    with pytest.raises(OSError, match="worker unavailable"):
        graph.invoke({"items": [1]})
