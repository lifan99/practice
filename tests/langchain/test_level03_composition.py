"""Level 3: check parallel branches, batch inputs, and explicit routing."""

from copy import deepcopy

import pytest
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable, RunnableLambda

from langchain_practice.level03_composition import build_parallel_analysis, build_router

pytestmark = pytest.mark.exercise


def test_parallel_analysis_and_batch():
    calls = []

    def model(branch, prompt):
        messages = prompt.to_messages()
        assert [message.type for message in messages] == ["system", "human"]
        expected = "Summarize the text." if branch == "summary" else "List three keywords."
        assert messages[0].content == expected
        calls.append((branch, messages[1].content))
        return AIMessage(content=f"{branch}:{messages[1].content}")

    chain = build_parallel_analysis(RunnableLambda(lambda p: model("summary", p)), RunnableLambda(lambda p: model("keywords", p)))
    assert isinstance(chain, Runnable)
    inputs = [{"text": "alpha"}, {"text": "beta"}]
    snapshot = deepcopy(inputs)
    assert chain.batch(inputs) == [{"summary": "summary:alpha", "keywords": "keywords:alpha"}, {"summary": "summary:beta", "keywords": "keywords:beta"}]
    assert sorted(calls) == [("keywords", "alpha"), ("keywords", "beta"), ("summary", "alpha"), ("summary", "beta")]
    assert inputs == snapshot


def test_parallel_missing_input():
    chain = build_parallel_analysis(RunnableLambda(lambda _: AIMessage(content="a")), RunnableLambda(lambda _: AIMessage(content="b")))
    with pytest.raises(KeyError):
        chain.invoke({})


def test_router_selects_only_one_branch_and_forwards_payload():
    calls = []

    def branch(label):
        return RunnableLambda(lambda value: calls.append((label, value)) or label)

    router = build_router({"a": branch("a"), "b": branch("b")}, branch("default"))
    payload = {"nested": [1, 2]}
    snapshot = deepcopy(payload)
    assert router.invoke({"route": "b", "payload": payload}) == "b"
    assert router.invoke({"route": "unknown", "payload": 7}) == "default"
    assert calls == [("b", payload), ("default", 7)]
    assert payload == snapshot


def test_empty_routes_use_default():
    assert build_router({}, RunnableLambda(lambda x: x * 2)).invoke({"route": "any", "payload": 3}) == 6


@pytest.mark.parametrize("inputs", [{"route": "a"}, {"payload": "x"}])
def test_router_requires_both_keys(inputs):
    router = build_router({}, RunnableLambda(lambda _: "default"))
    with pytest.raises(KeyError):
        router.invoke(inputs)
