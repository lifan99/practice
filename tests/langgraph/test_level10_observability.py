"""Level 10: check update envelopes, v3 values, pause, and cleanup."""

from typing import TypedDict

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from langgraph_practice.level10_observability import collect_updates, observe_run
from langgraph_practice.runtime_fixtures import create_probe_graph

pytestmark = pytest.mark.exercise


def test_collect_real_node_updates():
    assert collect_updates(create_probe_graph(), {"value": 3}) == [{"node": "double", "values": {"twice": 6}}, {"node": "finish", "values": {"result": 7}}]


def test_update_filtering_config_and_snapshot_copy():
    original = {"items": [1]}

    class GraphStub:
        def __init__(self):
            self.calls = []

        def stream(self, inputs, config=None, **kwargs):
            self.calls.append((inputs, config, kwargs))
            yield {"type": "values", "ns": (), "data": {"ignored": True}}
            yield {"type": "updates", "ns": (), "data": {"node": original, "__interrupt__": ("payload",), "empty": None}}

    graph = GraphStub()
    config = {"tags": ["practice"]}
    result = collect_updates(graph, {"input": 1}, config)
    original["items"].append(2)
    assert result == [{"node": "node", "values": {"items": [1]}}]
    assert len(graph.calls) == 1
    assert graph.calls[0][:2] == ({"input": 1}, config)
    assert graph.calls[0][2]["stream_mode"] == "updates" and graph.calls[0][2]["version"] == "v2"


def test_observe_complete_run_has_full_snapshots_and_output():
    report = observe_run(create_probe_graph(), {"value": 3})
    assert report["snapshots"] == [{"value": 3}, {"value": 3, "twice": 6}, {"value": 3, "twice": 6, "result": 7}]
    assert report["output"] == {"value": 3, "twice": 6, "result": 7}
    assert report["interrupted"] is False and report["interrupts"] == []


def test_observe_native_interrupt_is_not_reported_as_completion():
    class State(TypedDict, total=False):
        value: int
        approved: bool

    def pause(state):
        return {"approved": interrupt({"kind": "probe"})}

    builder = StateGraph(State)
    builder.add_node("pause", pause)
    builder.add_edge(START, "pause")
    builder.add_edge("pause", END)
    graph = builder.compile(checkpointer=InMemorySaver())
    config = {"configurable": {"thread_id": "observe-pause"}}
    report = observe_run(graph, {"value": 1}, config)
    assert report["interrupted"] is True and report["interrupts"] == [{"kind": "probe"}]
    assert report["output"] == {"value": 1}
    assert graph.get_state(config).next == ("pause",)


def test_event_context_closes_after_error():
    events = []

    class StreamStub:
        def __enter__(self):
            events.append("enter")
            return self

        def __exit__(self, *args):
            events.append("exit")

        @property
        def values(self):
            yield {"value": 1}
            raise OSError("node unavailable")

    class GraphStub:
        def stream_events(self, inputs, config=None, **kwargs):
            assert kwargs == {"version": "v3"}
            return StreamStub()

    with pytest.raises(OSError, match="node unavailable"):
        observe_run(GraphStub(), {})
    assert events == ["enter", "exit"]
