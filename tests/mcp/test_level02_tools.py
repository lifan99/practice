"""Level 2: use the real SDK client to discover and invoke student tools."""

import asyncio

import pytest
from mcp import Client
from mcp.server import MCPServer

from mcp_practice.exercises.level02_tools import build_calculator_server

pytestmark = pytest.mark.exercise


def test_tool_discovery_and_numeric_results():
    server = build_calculator_server()
    assert isinstance(server, MCPServer)

    async def exercise():
        async with Client(server, read_timeout_seconds=3) as client:
            tools = {tool.name: tool for tool in (await client.list_tools()).tools}
            assert set(tools) == {"add", "divide"}
            assert all(tool.description for tool in tools.values())
            assert tools["add"].input_schema["properties"]["a"]["type"] == "integer"
            assert sorted(tools["add"].input_schema["required"]) == ["a", "b"]
            assert (await client.call_tool("add", {"a": -2, "b": 5})).structured_content == {"result": 3}
            assert (await client.call_tool("divide", {"a": 5.0, "b": 2.0})).structured_content == {"result": 2.5}

    asyncio.run(asyncio.wait_for(exercise(), 12))


@pytest.mark.parametrize("name,arguments", [("add", {"a": "not an integer", "b": 2}), ("divide", {"a": 1, "b": 0})])
def test_tool_failures_remain_error_results(name, arguments):
    server = build_calculator_server()

    async def exercise():
        async with Client(server, read_timeout_seconds=3) as client:
            result = await client.call_tool(name, arguments)
            assert result.is_error is True
            if name == "divide":
                assert "nonzero" in "\n".join(block.text for block in result.content if block.type == "text")

    asyncio.run(asyncio.wait_for(exercise(), 10))
