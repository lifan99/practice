"""Level 7: inspect model history rather than trusting preset answers."""

import pytest
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from langchain_practice.exercises.level07_memory import build_memory_agent, chat
from langchain_practice.support.offline_models import ScriptedChatModel

pytestmark = pytest.mark.exercise


def test_memory_retains_same_thread_and_isolates_other_threads():
    model = ScriptedChatModel(responses=[AIMessage(content="ack A"), AIMessage(content="ack B"), AIMessage(content="ack A again")])
    agent = build_memory_agent(model, InMemorySaver())
    assert chat(agent, "A", "  Alice here  ") == "ack A"
    assert chat(agent, "B", "Bob here") == "ack B"
    assert chat(agent, "A", "What did I say?") == "ack A again"
    assert [m.content for m in model.recorded_messages[1] if m.type == "human"] == ["Bob here"]
    assert [m.content for m in model.recorded_messages[2] if m.type == "human"] == ["Alice here", "What did I say?"]
    assert [m.content for m in model.recorded_messages[2] if m.type == "ai"] == ["ack A"]
    assert all(messages[0].content == "You are a helpful tutor." for messages in model.recorded_messages)


def test_chat_passes_only_new_message_and_preserves_thread_id():
    class AgentStub:
        def __init__(self):
            self.calls = []

        def invoke(self, inputs, config):
            self.calls.append((inputs, config))
            return {"messages": [AIMessage(content="answer")]}

    agent = AgentStub()
    assert chat(agent, " thread A ", "  hello  ") == "answer"
    assert len(agent.calls) == 1
    inputs, config = agent.calls[0]
    assert len(inputs["messages"]) == 1
    assert isinstance(inputs["messages"][0], HumanMessage)
    assert inputs["messages"][0].content == "hello"
    assert config == {"configurable": {"thread_id": " thread A "}}


@pytest.mark.parametrize("thread_id,text", [(" ", "hello"), ("A", " \n")])
def test_invalid_chat_does_not_invoke(thread_id, text):
    class ForbiddenAgent:
        def invoke(self, *args, **kwargs):
            pytest.fail("Invalid chat input must not invoke the agent.")

    with pytest.raises(ValueError):
        chat(ForbiddenAgent(), thread_id, text)
