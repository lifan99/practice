"""Level 5: check tool dispatch IDs, validation, and serialization."""

from copy import deepcopy

import pytest
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool

from langchain_practice.level05_tool_protocol import execute_tool_calls

pytestmark = pytest.mark.exercise


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


@tool
def describe(name: str) -> dict:
    """Return a small structured description."""
    return {"z": 2, "name": name}


def test_tool_batch_preserves_ids_names_and_message():
    message = AIMessage(content="", tool_calls=[
        {"name": "add", "args": {"a": 2, "b": 3}, "id": "call-1", "type": "tool_call"},
        {"name": "describe", "args": {"name": "中文"}, "id": "call-2", "type": "tool_call"},
    ])
    snapshot = deepcopy(message)
    results = execute_tool_calls(message, [add, describe])
    assert all(isinstance(result, ToolMessage) for result in results)
    assert [(r.name, r.tool_call_id, r.content) for r in results] == [("add", "call-1", "5"), ("describe", "call-2", '{"name": "中文", "z": 2}')]
    assert message == snapshot


def test_no_calls():
    assert execute_tool_calls(AIMessage(content="done"), [add]) == []


def test_duplicate_tool_names_invalid_even_without_calls():
    with pytest.raises(ValueError):
        execute_tool_calls(AIMessage(content="done"), [add, add])


@pytest.mark.parametrize("bad_id", ["", None, "first"])
def test_invalid_call_ids_are_checked_before_execution(bad_id):
    calls = []

    @tool
    def record(value: int) -> int:
        """Record a local integer."""
        calls.append(value)
        return value

    message = AIMessage(content="", tool_calls=[
        {"name": "record", "args": {"value": 1}, "id": "first", "type": "tool_call"},
        {"name": "record", "args": {"value": 2}, "id": bad_id, "type": "tool_call"},
    ])
    with pytest.raises(ValueError):
        execute_tool_calls(message, [record])
    assert calls == []


def test_unknown_tool_is_checked_before_execution():
    calls = []

    @tool
    def record(value: int) -> int:
        """Record a local integer."""
        calls.append(value)
        return value

    message = AIMessage(content="", tool_calls=[
        {"name": "record", "args": {"value": 1}, "id": "first", "type": "tool_call"},
        {"name": "unknown", "args": {}, "id": "second", "type": "tool_call"},
    ])
    with pytest.raises(KeyError) as caught:
        execute_tool_calls(message, [record])
    assert caught.value.args[0] == "unknown"
    assert calls == []


def test_tool_failure_propagates():
    @tool
    def fail(value: int) -> int:
        """Raise a local dependency failure."""
        raise OSError("tool unavailable")

    message = AIMessage(content="", tool_calls=[{"name": "fail", "args": {"value": 1}, "id": "call-1", "type": "tool_call"}])
    with pytest.raises(OSError, match="tool unavailable"):
        execute_tool_calls(message, [fail])
