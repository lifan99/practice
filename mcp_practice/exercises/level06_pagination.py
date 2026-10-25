"""Level 6: discover tools across opaque cursor pages with bounded work."""

from mcp import Client
from mcp_types import Tool


class PaginationError(RuntimeError):
    """The server repeated a cursor or exceeded the permitted page count."""


async def list_all_tools(client: Client, max_pages: int = 20) -> list[Tool]:
    """Collect tool pages without interpreting cursor contents."""
    raise NotImplementedError("TODO MCP-L6: implement list_all_tools")
