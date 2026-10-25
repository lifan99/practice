"""Level 1: inspect tool descriptors and interpret tool-result content."""

from typing import TypedDict

from mcp_types import CallToolResult, Tool


class ToolSummary(TypedDict):
    name: str
    description: str
    required: list[str]


class ToolCallFailed(RuntimeError):
    """A tool returned a protocol result whose is_error flag is true."""


def summarize_tools(tools: list[Tool]) -> list[ToolSummary]:
    """Return sorted tool names, descriptions, and required argument names."""
    raise NotImplementedError("TODO MCP-L1A: implement summarize_tools")


def tool_text(result: CallToolResult) -> str:
    """Extract text blocks while keeping failed tool results distinguishable."""
    raise NotImplementedError("TODO MCP-L1B: implement tool_text")
