"""Level 3: provide static resources, URI templates, and prompts."""

from mcp.server import MCPServer


def build_notes_server(notes: dict[str, str]) -> MCPServer:
    """Expose a note catalog, note resources, and a study-note prompt."""
    raise NotImplementedError("TODO MCP-L3: implement build_notes_server")
