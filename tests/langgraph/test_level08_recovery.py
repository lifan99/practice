"""Level 8: check selective retries and checkpoint-based resumption."""

import pytest
from langgraph.checkpoint.memory import InMemorySaver

from langgraph_practice.level08_recovery import build_recoverable_graph

pytestmark = pytest.mark.exercise


def test_timeout_retry_does_not_repeat_preparation():
    calls = []

    def prepare(payload):
        calls.append(("prepare", payload))
        return "prepared:" + payload

    def deliver(prepared):
        calls.append(("deliver", prepared))
        if sum(name == "deliver" for name, _ in calls) == 1:
            raise TimeoutError("temporary")
        return "receipt"

    graph = build_recoverable_graph(InMemorySaver(), prepare, deliver, 2)
    result = graph.invoke({"payload": "  payload  "}, {"configurable": {"thread_id": "retry"}})
    assert result["receipt"] == "receipt"
    assert calls == [("prepare", "payload"), ("deliver", "prepared:payload"), ("deliver", "prepared:payload")]


def test_external_resume_only_reruns_failed_node():
    calls = []

    def prepare(payload):
        calls.append("prepare")
        return "ready"

    def deliver(prepared):
        assert prepared == "ready"
        calls.append("deliver")
        if calls.count("deliver") == 1:
            raise OSError("dependency unavailable")
        return "receipt"

    graph = build_recoverable_graph(InMemorySaver(), prepare, deliver, 3)
    config = {"configurable": {"thread_id": "resume"}}
    with pytest.raises(OSError, match="dependency unavailable"):
        graph.invoke({"payload": "input"}, config)
    assert calls == ["prepare", "deliver"]
    assert graph.get_state(config).values["prepared"] == "ready"
    assert graph.get_state(config).next == ("deliver",)
    assert graph.invoke(None, config)["receipt"] == "receipt"
    assert calls == ["prepare", "deliver", "deliver"]


@pytest.mark.parametrize("attempts", [1, 3])
def test_retry_exhaustion_preserves_error(attempts):
    calls = []

    def fail(_):
        calls.append("deliver")
        raise TimeoutError("still unavailable")

    graph = build_recoverable_graph(InMemorySaver(), lambda _: "ready", fail, attempts)
    with pytest.raises(TimeoutError, match="still unavailable"):
        graph.invoke({"payload": "input"}, {"configurable": {"thread_id": "exhausted"}})
    assert len(calls) == attempts


@pytest.mark.parametrize("attempts", [0, -1])
def test_invalid_retry_configuration(attempts):
    with pytest.raises(ValueError):
        build_recoverable_graph(InMemorySaver(), lambda x: x, lambda x: x, attempts)


def test_blank_payload_calls_no_callbacks():
    def forbidden(_):
        pytest.fail("Blank payload must not execute callbacks.")

    graph = build_recoverable_graph(InMemorySaver(), forbidden, forbidden)
    with pytest.raises(ValueError):
        graph.invoke({"payload": " "}, {"configurable": {"thread_id": "blank"}})
