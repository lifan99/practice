"""Level 3: verify resource templates and prompt messages through MCP."""

import asyncio

import pytest
from mcp import Client
from mcp.shared.exceptions import MCPError

from mcp_practice.level03_context import build_notes_server

pytestmark = pytest.mark.exercise


def test_resources_and_prompts_use_original_note_snapshot():
    notes = {"z": "Last note.", "intro": "First note.\n"}
    server = build_notes_server(notes)
    notes["intro"] = "Changed after construction."

    async def exercise():
        async with Client(server, read_timeout_seconds=3) as client:
            assert "notes://catalog" in [str(resource.uri) for resource in (await client.list_resources()).resources]
            assert "note://{name}" in [template.uri_template for template in (await client.list_resource_templates()).resource_templates]
            assert (await client.read_resource("notes://catalog")).contents[0].text == "intro\nz"
            resource = (await client.read_resource("note://intro")).contents[0]
            assert resource.text == "First note.\n" and resource.mime_type == "text/plain"
            assert "study_note" in [prompt.name for prompt in (await client.list_prompts()).prompts]
            messages = (await client.get_prompt("study_note", {"name": "intro"})).messages
            assert len(messages) == 1 and messages[0].role == "user"
            assert messages[0].content.text == "Explain this note:\nFirst note.\n"

    asyncio.run(asyncio.wait_for(exercise(), 15))


def test_unknown_note_is_an_sdk_error():
    server = build_notes_server({})

    async def exercise():
        async with Client(server, read_timeout_seconds=3) as client:
            with pytest.raises(MCPError):
                await client.read_resource("note://unknown")
            with pytest.raises(MCPError):
                await client.get_prompt("study_note", {"name": "unknown"})

    asyncio.run(asyncio.wait_for(exercise(), 10))
