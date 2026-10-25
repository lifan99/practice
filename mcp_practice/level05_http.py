"""Level 5: expose an SDK server as a Streamable HTTP ASGI app."""

from mcp.server import MCPServer
from starlette.applications import Starlette


def build_http_app(server: MCPServer) -> Starlette:
    """Build the SDK's /mcp endpoint with JSON responses and stateless HTTP."""
    raise NotImplementedError("TODO MCP-L5: implement build_http_app")
