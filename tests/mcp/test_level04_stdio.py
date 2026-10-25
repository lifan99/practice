"""Level 4: probe a real subprocess and independently check cleanup."""

import asyncio
import sys
from pathlib import Path

import pytest
from mcp import StdioServerParameters
from mcp_types import ListToolsResult, ReadResourceResult, TextResourceContents, Tool

from mcp_practice import level04_stdio as stdio

pytestmark = pytest.mark.exercise


def parameters():
    return StdioServerParameters(command=sys.executable, args=["-m", "mcp_practice.reference_server"], cwd=Path(__file__).resolve().parents[2])


def test_real_stdio_server_round_trip():
    assert asyncio.run(asyncio.wait_for(stdio.inspect_stdio(parameters()), 12)) == {"tools": ["echo"], "echo": "hello", "health": "ready"}


def test_stdio_context_closes_on_call_failure(monkeypatch):
    events = []

    class FailingClient:
        def __init__(self, server, **kwargs):
            events.append("created")

        async def __aenter__(self):
            events.append("opened")
            return self

        async def __aexit__(self, *args):
            events.append("closed")

        async def list_tools(self, **kwargs):
            return ListToolsResult(tools=[Tool(name="echo", input_schema={"type": "object"})])

        async def call_tool(self, *args, **kwargs):
            raise OSError("call unavailable")

        async def read_resource(self, *args, **kwargs):
            return ReadResourceResult(contents=[TextResourceContents(uri="health://ready", text="ready")])

    monkeypatch.setattr(stdio, "Client", FailingClient)
    with pytest.raises(OSError, match="call unavailable"):
        asyncio.run(stdio.inspect_stdio(parameters()))
    assert events == ["created", "opened", "closed"]
