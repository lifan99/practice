"""Level 7: check call scheduling, timeouts, cancellation, and progress."""

import asyncio

import pytest
from mcp import Client
from mcp_types import CallToolResult, TextContent

from mcp_practice.level07_execution import ToolCall, build_progress_server, call_tools_bounded

pytestmark = pytest.mark.exercise


def test_bounded_calls_preserve_results_and_error_kinds():
    async def exercise():
        active = peak = 0
        error = OSError("transport unavailable")
        tool_error = CallToolResult(content=[TextContent(type="text", text="rejected")], is_error=True)

        class ClientStub:
            async def call_tool(self, name, arguments):
                nonlocal active, peak
                active += 1
                peak = max(peak, active)
                try:
                    await asyncio.sleep(0)
                    if name == "network":
                        raise error
                    if name == "business":
                        return tool_error
                    return CallToolResult(content=[], structured_content=arguments)
                finally:
                    active -= 1

        calls = [ToolCall("ok", {"n": 1}), ToolCall("business", {}), ToolCall("network", {}), ToolCall("ok", {"n": 4})]
        result = await call_tools_bounded(ClientStub(), calls, 2, 1.0)
        assert result[0].structured_content == {"n": 1}
        assert result[1] is tool_error and result[2] is error
        assert result[3].structured_content == {"n": 4}
        assert peak == 2 and active == 0

    asyncio.run(exercise())


def test_empty_call_batch():
    assert asyncio.run(call_tools_bounded(None, [], 1, 1.0)) == []


def test_per_call_timeout_cleans_up_underlying_wait():
    async def exercise():
        cleaned = asyncio.Event()

        class WaitingClient:
            async def call_tool(self, name, arguments):
                try:
                    await asyncio.Event().wait()
                finally:
                    cleaned.set()

        result = await call_tools_bounded(WaitingClient(), [ToolCall("wait", {})], 1, 0.01)
        assert isinstance(result[0], TimeoutError)
        assert cleaned.is_set()

    asyncio.run(asyncio.wait_for(exercise(), 2))


def test_outer_cancellation_cleans_up_started_calls():
    async def exercise():
        started, cleaned = asyncio.Event(), asyncio.Event()

        class WaitingClient:
            async def call_tool(self, name, arguments):
                started.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    cleaned.set()

        task = asyncio.create_task(call_tools_bounded(WaitingClient(), [ToolCall("wait", {})], 1, 5.0))
        try:
            await asyncio.wait_for(started.wait(), 0.2)
        except TimeoutError:
            await task
            raise
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert cleaned.is_set()

    asyncio.run(asyncio.wait_for(exercise(), 2))


@pytest.mark.parametrize("concurrency,timeout", [(0, 1.0), (1, 0.0), (1, float("nan")), (1, float("inf"))])
def test_invalid_limits(concurrency, timeout):
    with pytest.raises(ValueError):
        asyncio.run(call_tools_bounded(None, [], concurrency, timeout))


def test_progress_is_typed_ordered_and_optional():
    server = build_progress_server()

    async def exercise():
        reports = []

        async def progress(value, total, message):
            reports.append((value, total, message))

        async with Client(server, read_timeout_seconds=3) as client:
            descriptor = (await client.list_tools()).tools[0]
            assert descriptor.name == "count_steps"
            assert set(descriptor.input_schema["properties"]) == {"steps"}
            result = await client.call_tool("count_steps", {"steps": 3}, progress_callback=progress)
            assert result.structured_content == {"result": 3}
            assert reports == [(1, 3, "step 1"), (2, 3, "step 2"), (3, 3, "step 3")]
            assert (await client.call_tool("count_steps", {"steps": 1})).structured_content == {"result": 1}
            reports.clear()
            assert (await client.call_tool("count_steps", {"steps": 0}, progress_callback=progress)).is_error is True
            assert reports == []

    asyncio.run(asyncio.wait_for(exercise(), 12))
