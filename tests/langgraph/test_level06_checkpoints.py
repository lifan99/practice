"""Level 6: inspect actual checkpoint state and isolate thread histories."""

from types import SimpleNamespace

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import CompiledStateGraph

from langgraph_practice.level06_checkpoints import build_counter_graph, counter_snapshot

pytestmark = pytest.mark.exercise


def test_counter_uses_injected_checkpointer_and_thread_state():
    saver = InMemorySaver()
    graph = build_counter_graph(saver)
    assert isinstance(graph, CompiledStateGraph)
    a, b = {"configurable": {"thread_id": "A"}}, {"configurable": {"thread_id": "B"}}
    assert graph.invoke({"delta": 3}, a)["total"] == 3
    assert graph.invoke({"delta": 4}, a)["total"] == 7
    assert graph.invoke({"delta": 2}, b)["total"] == 2
    assert graph.invoke({"delta": -1}, a)["total"] == 6
    assert graph.get_state(a).values["total"] == 6
    rebuilt = build_counter_graph(saver)
    assert rebuilt.invoke({"delta": 1}, a)["total"] == 7
    assert counter_snapshot(rebuilt, "A")["total"] == 7
    assert counter_snapshot(rebuilt, "missing") == {}


def test_snapshot_reads_without_invoking_and_returns_a_copy():
    class GraphStub:
        def __init__(self):
            self.values, self.configs = {"total": 7}, []

        def get_state(self, config):
            self.configs.append(config)
            return SimpleNamespace(values=self.values)

        def invoke(self, *args, **kwargs):
            pytest.fail("Reading a snapshot must not execute the graph.")

    graph = GraphStub()
    result = counter_snapshot(graph, " A ")
    result["total"] = 999
    assert graph.values == {"total": 7}
    assert graph.configs == [{"configurable": {"thread_id": " A "}}]


def test_blank_snapshot_thread_is_invalid():
    with pytest.raises(ValueError):
        counter_snapshot(None, " \n")
