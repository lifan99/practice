"""Level 8: implement an application boundary for file-backed resources."""

from pathlib import Path


def resolve_note_path(root: Path, relative_path: str) -> Path:
    """Resolve an existing Markdown file strictly within the note root."""
    raise NotImplementedError("TODO MCP-L8A: implement resolve_note_path")


def read_note(root: Path, relative_path: str) -> str:
    """Read a permitted Markdown file as UTF-8 without stripping content."""
    raise NotImplementedError("TODO MCP-L8B: implement read_note")
