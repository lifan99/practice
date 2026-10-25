"""Provided transport fixture, independent of all exercise implementations."""

from mcp.server import MCPServer


def create_reference_server() -> MCPServer:
    server = MCPServer("Practice reference")

    @server.tool()
    async def echo(message: str) -> str:
        """Echo one text message."""
        return message

    @server.resource("health://ready")
    async def health() -> str:
        """Report fixture readiness."""
        return "ready"

    return server


if __name__ == "__main__":
    create_reference_server().run(transport="stdio")
