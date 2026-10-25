"""Level 7: check native interruption, explicit decisions, and isolation."""

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command

from langgraph_practice.level07_interrupts import build_approval_graph

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("approved", [True, False])
def test_approval_pauses_before_action_and_resumes_explicitly(approved):
    calls = []
    graph = build_approval_graph(InMemorySaver(), lambda draft: calls.append(draft) or "receipt")
    assert isinstance(graph, CompiledStateGraph)
    config = {"configurable": {"thread_id": "approval"}}
    initial = {"draft": "  draft  "}
    paused = graph.invoke(initial, config)
    assert calls == [] and initial == {"draft": "  draft  "}
    assert paused["__interrupt__"][0].value == {"kind": "approval", "draft": "draft"}
    assert graph.get_state(config).next == ("review",)
    result = graph.invoke(Command(resume=approved), config)
    assert result["approved"] is approved
    assert result["status"] == ("published" if approved else "rejected")
    assert result["receipt"] == ("receipt" if approved else "")
    assert calls == (["draft"] if approved else [])
    assert graph.get_state(config).next == ()


@pytest.mark.parametrize("decision", ["yes", 1, {"approved": True}])
def test_non_boolean_resume_value_is_invalid(decision):
    calls = []
    graph = build_approval_graph(InMemorySaver(), lambda draft: calls.append(draft) or "receipt")
    config = {"configurable": {"thread_id": "invalid"}}
    graph.invoke({"draft": "draft"}, config)
    with pytest.raises(ValueError):
        graph.invoke(Command(resume=decision), config)
    assert calls == []


def test_pending_approvals_do_not_cross_threads():
    calls = []
    graph = build_approval_graph(InMemorySaver(), lambda draft: calls.append(draft) or "receipt")
    a, b = {"configurable": {"thread_id": "A"}}, {"configurable": {"thread_id": "B"}}
    graph.invoke({"draft": "first"}, a)
    graph.invoke({"draft": "second"}, b)
    graph.invoke(Command(resume=True), a)
    assert calls == ["first"]
    assert graph.get_state(b).next == ("review",)


def test_blank_draft_is_invalid_before_interrupt():
    graph = build_approval_graph(InMemorySaver(), lambda _: pytest.fail("Blank draft must not publish."))
    with pytest.raises(ValueError):
        graph.invoke({"draft": " \n"}, {"configurable": {"thread_id": "blank"}})


def test_publish_failure_propagates_after_approval():
    def fail(_):
        raise OSError("publish unavailable")

    graph = build_approval_graph(InMemorySaver(), fail)
    config = {"configurable": {"thread_id": "failure"}}
    graph.invoke({"draft": "draft"}, config)
    with pytest.raises(OSError, match="publish unavailable"):
        graph.invoke(Command(resume=True), config)
