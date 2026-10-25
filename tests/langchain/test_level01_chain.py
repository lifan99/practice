"""Public behavior checks for this exercise level."""

import pytest
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from langchain_practice.exercises.level01_chain import build_chain
from support.offline import fake_chat_model
pytestmark = pytest.mark.exercise


def test_chain_formats_messages_and_parses_output():
    captured = []

    def capture(prompt):
        captured.extend(prompt.to_messages())
        return AIMessage(content="A concise explanation.")

    chain = build_chain(RunnableLambda(capture))
    assert chain.invoke({"topic": "recursion", "audience": "beginner"}) == "A concise explanation."
    assert [message.type for message in captured] == ["system", "human"]
    assert captured[0].content == "You are a concise tutor. Reply in English."
    assert captured[1].content == "Explain recursion for a beginner."


def test_chain_uses_injected_model_and_new_inputs():
    chain = build_chain(fake_chat_model("first", "second"))
    assert chain.invoke({"topic": "graphs", "audience": "student"}) == "first"
    assert chain.invoke({"topic": "RAG", "audience": "developer"}) == "second"


@pytest.mark.parametrize("inputs", [{"topic": "RAG"}, {"audience": "student"}])
def test_chain_rejects_missing_variables(inputs):
    chain = build_chain(fake_chat_model("unused"))
    with pytest.raises(KeyError):
        chain.invoke(inputs)

