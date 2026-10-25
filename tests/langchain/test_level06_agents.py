"""Level 6: exercise the native agent using scripted tool requests."""

import pytest
from langchain.agents.middleware import before_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph.state import CompiledStateGraph

from langchain_practice.exercises.level06_agents import build_tool_agent
from langchain_practice.support.offline_models import ScriptedChatModel

pytestmark = pytest.mark.exercise


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


def test_native_agent_executes_multiple_tool_rounds():
    model = ScriptedChatModel(responses=[
        AIMessage(content="", tool_calls=[{"name": "add", "args": {"a": 2, "b": 3}, "id": "sum", "type": "tool_call"}]),
        AIMessage(content="", tool_calls=[{"name": "multiply", "args": {"a": 5, "b": 4}, "id": "product", "type": "tool_call"}]),
        AIMessage(content="20"),
    ])
    agent = build_tool_agent(model, [add, multiply])
    assert isinstance(agent, CompiledStateGraph)
    result = agent.invoke({"messages": [HumanMessage(content="Compute (2 + 3) * 4.")]})
    assert [message.type for message in result["messages"]] == ["human", "ai", "tool", "ai", "tool", "ai"]
    tool_results = [message for message in result["messages"] if message.type == "tool"]
    assert [(message.tool_call_id, message.content) for message in tool_results] == [("sum", "5"), ("product", "20")]
    assert result["messages"][-1].content == "20"
    assert model.calls == 3
    assert set(model.bound_tool_names) == {"add", "multiply"}
    assert model.recorded_messages[0][0].content == "Use tools when needed. Never invent tool results."


def test_agent_accepts_middleware_in_original_order():
    calls = []

    @before_model
    def first(state, runtime):
        calls.append("first")
        return None

    @before_model
    def second(state, runtime):
        calls.append("second")
        return None

    agent = build_tool_agent(ScriptedChatModel(responses=[AIMessage(content="done")]), [], [first, second])
    assert agent.invoke({"messages": [HumanMessage(content="hello")]})["messages"][-1].content == "done"
    assert calls == ["first", "second"]


def test_agent_rejects_duplicate_tools():
    with pytest.raises(ValueError):
        build_tool_agent(ScriptedChatModel(responses=[]), [add, add])
