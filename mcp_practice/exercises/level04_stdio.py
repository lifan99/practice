"""Level 4: manage a real local MCP subprocess with the v2 Client."""

from typing import TypedDict

from mcp import Client, StdioServerParameters


class StdioReport(TypedDict):
    tools: list[str]
    echo: str
    health: str


async def inspect_stdio(server: StdioServerParameters) -> StdioReport:
    """Discover and probe the provided local reference server."""
    raise NotImplementedError("TODO MCP-L4: implement inspect_stdio")
