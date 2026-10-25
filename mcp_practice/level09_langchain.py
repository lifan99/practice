"""Level 9: adapt a connected MCP client's tools to async LangChain tools."""

from mcp import Client
from mcp_types import Tool
from langchain_core.tools import StructuredTool

from . import level01_protocol


def make_langchain_tools(client: Client, tools: list[Tool]) -> list[StructuredTool]:
    """Preserve argument schemas and attach raw MCP results as artifacts."""
    raise NotImplementedError("TODO MCP-L9: implement make_langchain_tools")
