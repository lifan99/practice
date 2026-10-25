"""Public behavior checks for this exercise level."""

import pytest
from langchain_core.exceptions import OutputParserException
from langchain_core.tools import BaseTool
from langchain_practice.exercises.level02_tools import StudyPlan, make_word_count_tool, parse_study_plan
pytestmark = pytest.mark.exercise


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

