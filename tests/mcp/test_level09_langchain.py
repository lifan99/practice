"""Level 9: keep MCP schemas, async calls, and raw protocol artifacts."""

import asyncio

import pytest
from langchain_core.messages import ToolMessage
from langchain_core.tools import StructuredTool, ToolException
from mcp_types import CallToolResult, TextContent, Tool

from mcp_practice.exercises import level01_protocol
from mcp_practice.exercises.level09_langchain import make_langchain_tools

pytestmark = pytest.mark.exercise


def descriptors():
    return [Tool(name=name, description=None, input_schema={"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}) for name in ["first", "second"]]


def test_adapters_keep_distinct_names_schemas_and_artifacts(monkeypatch):
    calls, decoded = [], []
    raw = CallToolResult(content=[TextContent(type="text", text="raw reply")])

    class ClientStub:
        async def call_tool(self, name, arguments):
            calls.append((name, arguments))
            return raw

    def decode(result):
        decoded.append(result)
        return "decoded reply"

    monkeypatch.setattr(level01_protocol, "tool_text", decode)
    tools = make_langchain_tools(ClientStub(), descriptors())
    assert all(isinstance(tool, StructuredTool) for tool in tools)
    assert [tool.name for tool in tools] == ["first", "second"]
    assert tools[0].args == {"text": {"type": "string"}}
    assert tools[0].description == "MCP tool first."

    async def exercise():
        for i, tool in enumerate(tools):
            result = await tool.ainvoke({"name": tool.name, "args": {"text": f"value-{i}"}, "id": f"call-{i}", "type": "tool_call"})
            assert isinstance(result, ToolMessage)
            assert result.content == "decoded reply" and result.artifact is raw
            assert result.tool_call_id == f"call-{i}"

    asyncio.run(exercise())
    assert calls == [("first", {"text": "value-0"}), ("second", {"text": "value-1"})]
    assert decoded == [raw, raw]


def test_mcp_business_error_becomes_tool_exception(monkeypatch):
    class ClientStub:
        async def call_tool(self, *args, **kwargs):
            return CallToolResult(content=[TextContent(type="text", text="rejected")], is_error=True)

    def forbidden(_):
        pytest.fail("A failed MCP result must not be decoded as successful content.")

    monkeypatch.setattr(level01_protocol, "tool_text", forbidden)
    tool = make_langchain_tools(ClientStub(), descriptors()[:1])[0]
    with pytest.raises(ToolException):
        asyncio.run(tool.ainvoke({"text": "request"}))


def test_mcp_transport_error_propagates():
    class ClientStub:
        async def call_tool(self, *args, **kwargs):
            raise OSError("connection unavailable")

    tool = make_langchain_tools(ClientStub(), descriptors()[:1])[0]
    with pytest.raises(OSError, match="connection unavailable"):
        asyncio.run(tool.ainvoke({"text": "request"}))


def test_duplicate_mcp_names_rejected():
    descriptor = descriptors()[0]
    with pytest.raises(ValueError):
        make_langchain_tools(None, [descriptor, descriptor])
