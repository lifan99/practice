"""Public behavior checks for the LangChain exercises."""

import pytest
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import BaseTool

from langchain_practice.ex01_chain import build_chain
from langchain_practice.ex02_tools import StudyPlan, make_word_count_tool, parse_study_plan
from practice_support import fake_chat_model

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


@pytest.mark.parametrize("text,expected", [("one two", 2), ("  one\n two\tthree  ", 3), (" \t\n", 0), ("", 0)])
def test_word_count_tool(text, expected):
    tool = make_word_count_tool()
    assert isinstance(tool, BaseTool)
    assert tool.name == "word_count"
    assert tool.description.strip()
    assert "text" in tool.args
    assert tool.invoke({"text": text}) == expected


def test_plan_parser_returns_validated_model():
    plan = parse_study_plan('{"topic":"RAG","steps":["Read","Build"],"minutes":30}')
    assert isinstance(plan, StudyPlan)
    assert plan.model_dump() == {"topic": "RAG", "steps": ["Read", "Build"], "minutes": 30}


@pytest.mark.parametrize("text", [
    "not JSON",
    '{"topic":"RAG","steps":[],"minutes":30}',
    '{"topic":"RAG","steps":["a","b","c","d"],"minutes":30}',
    '{"topic":"","steps":["Read"],"minutes":30}',
    '{"topic":"RAG","steps":["Read"],"minutes":0}',
    '{"topic":"RAG","steps":["Read"],"minutes":121}',
    '{"topic":"RAG"}',
])
def test_plan_parser_exposes_invalid_output(text):
    with pytest.raises(OutputParserException):
        parse_study_plan(text)
