"""Level 8: check retry boundaries and recoverable tool middleware."""

from types import SimpleNamespace

import pytest
from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda

from langchain_practice.exercises.level08_reliability import build_resilient_chain, make_tool_error_middleware

pytestmark = pytest.mark.exercise


def test_timeout_recovers_before_fallback_and_preserves_config():
    calls = []

    def primary(value, config):
        calls.append((value, config))
        if len(calls) == 1:
            raise TimeoutError("temporary")
        return "primary answer"

    def forbidden(_):
        pytest.fail("Recovered primary must not fall back.")

    chain = build_resilient_chain(RunnableLambda(primary), RunnableLambda(forbidden), 2)
    assert chain.invoke({"q": "test"}, config={"tags": ["practice"], "metadata": {"case": "retry"}}) == "primary answer"
    assert len(calls) == 2
    assert all(value == {"q": "test"} and "practice" in config["tags"] and config["metadata"]["case"] == "retry" for value, config in calls)


def test_fallback_runs_once_after_primary_attempt_limit():
    calls = []

    def primary(value):
        calls.append(("primary", value))
        raise TimeoutError("temporary")

    def fallback(value):
        calls.append(("fallback", value))
        return "fallback answer"

    chain = build_resilient_chain(RunnableLambda(primary), RunnableLambda(fallback), 3)
    assert chain.invoke("q") == "fallback answer"
    assert calls == [("primary", "q")] * 3 + [("fallback", "q")]


def test_non_timeout_error_does_not_retry_or_fallback():
    calls = []

    def fail(value):
        calls.append(value)
        raise OSError("service unavailable")

    def forbidden(_):
        pytest.fail("Other exceptions must not fall back.")

    chain = build_resilient_chain(RunnableLambda(fail), RunnableLambda(forbidden), 3)
    with pytest.raises(OSError, match="service unavailable"):
        chain.invoke("q")
    assert calls == ["q"]


@pytest.mark.parametrize("attempts", [0, -1])
def test_invalid_attempt_limit(attempts):
    with pytest.raises(ValueError):
        build_resilient_chain(RunnableLambda(lambda x: x), RunnableLambda(lambda x: x), attempts)


def request():
    return SimpleNamespace(tool_call={"name": "calculate", "args": {}, "id": "tool-1", "type": "tool_call"})


def test_tool_middleware_returns_normal_result_without_replacement():
    middleware = make_tool_error_middleware()
    assert isinstance(middleware, AgentMiddleware)
    result = ToolMessage(content="42", tool_call_id="tool-1", name="calculate")
    calls = []
    req = request()

    def handler(value):
        calls.append(value)
        return result

    assert middleware.wrap_tool_call(req, handler) is result
    assert calls == [req]


def test_tool_middleware_marks_rejected_input_as_error():
    middleware = make_tool_error_middleware()
    calls = []

    def handler(req):
        calls.append(req)
        raise ValueError("invalid argument")

    req = request()
    result = middleware.wrap_tool_call(req, handler)
    assert isinstance(result, ToolMessage)
    assert (result.content, result.name, result.tool_call_id, result.status) == ("Tool input rejected.", "calculate", "tool-1", "error")
    assert calls == [req]


def test_tool_middleware_propagates_dependency_error():
    middleware = make_tool_error_middleware()

    def handler(_):
        raise OSError("tool unavailable")

    with pytest.raises(OSError, match="tool unavailable"):
        middleware.wrap_tool_call(request(), handler)
