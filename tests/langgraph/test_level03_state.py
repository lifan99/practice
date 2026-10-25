"""Level 3: check ID-aware reducer behavior and graph message updates."""

from copy import deepcopy

import pytest
from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage
from langgraph.graph.state import CompiledStateGraph

from langgraph_practice.exercises.level03_state import build_message_graph, merge_messages

pytestmark = pytest.mark.exercise


def test_message_updates_replace_append_and_remove_without_mutation():
    old = [HumanMessage(content="question", id="u1"), AIMessage(content="old", id="a1")]
    updates = [AIMessage(content="revised", id="a1"), HumanMessage(content="next", id="u2")]
    snapshot = deepcopy((old, updates))
    merged = merge_messages(old, updates)
    assert [(m.id, m.content) for m in merged] == [("u1", "question"), ("a1", "revised"), ("u2", "next")]
    assert [(m.id, m.content) for m in merge_messages(merged, [RemoveMessage(id="a1")])] == [("u1", "question"), ("u2", "next")]
    assert (old, updates) == snapshot


def test_auto_ids_do_not_mutate_input_messages():
    message = HumanMessage(content="question")
    merged = merge_messages([], [message])
    assert message.id is None
    assert merged[0].id is not None and merged[0].content == "question"


def test_removing_missing_message_is_invalid():
    with pytest.raises(ValueError):
        merge_messages([], [RemoveMessage(id="missing")])


def test_message_graph_applies_reducer_and_has_no_implicit_history():
    calls = []

    def responder(messages):
        calls.append(deepcopy(messages))
        return AIMessage(content="reply", id="answer")

    graph = build_message_graph(responder)
    assert isinstance(graph, CompiledStateGraph)
    initial = {"messages": [HumanMessage(content="question", id="u1"), AIMessage(content="old", id="answer")]}
    snapshot = deepcopy(initial)
    result = graph.invoke(initial)
    assert [(m.id, m.content) for m in result["messages"]] == [("u1", "question"), ("answer", "reply")]
    second = graph.invoke({"messages": [HumanMessage(content="fresh", id="u2")]})
    assert [m.content for m in second["messages"]] == ["fresh", "reply"]
    assert len(calls) == 2 and len(calls[1]) == 1
    assert initial == snapshot


def test_empty_message_input_does_not_respond():
    def forbidden(_):
        pytest.fail("Empty input must not call responder.")

    graph = build_message_graph(forbidden)
    with pytest.raises(ValueError):
        graph.invoke({"messages": []})
