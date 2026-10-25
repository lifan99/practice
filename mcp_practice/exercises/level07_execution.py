"""Level 7: bound client work and provide cooperative server progress."""

from dataclasses import dataclass
from typing import Any

from mcp import Client
from mcp.server import MCPServer
from mcp_types import CallToolResult


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]


async def call_tools_bounded(
    client: Client,
    calls: list[ToolCall],
    max_concurrency: int = 2,
    timeout_seconds: float = 5.0,
) -> list[CallToolResult | Exception]:
    """Return ordered results with per-call deadlines and error isolation."""
    raise NotImplementedError("TODO MCP-L7A: implement call_tools_bounded")


def build_progress_server() -> MCPServer:
    """Register count_steps with injected Context and incremental progress."""
    raise NotImplementedError("TODO MCP-L7B: implement build_progress_server")
