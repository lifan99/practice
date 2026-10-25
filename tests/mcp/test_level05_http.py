"""Level 5: test actual Streamable HTTP protocol handling without sockets."""

import asyncio

import pytest
from starlette.applications import Starlette

from mcp_practice.level05_http import build_http_app
from mcp_practice.reference_server import create_reference_server
from mcp_practice.test_support import client_for_app

pytestmark = pytest.mark.exercise


def test_mcp_http_endpoint_round_trip():
    app = build_http_app(create_reference_server())
    assert isinstance(app, Starlette)

    async def exercise():
        async with client_for_app(app) as client:
            assert [tool.name for tool in (await client.list_tools()).tools] == ["echo"]
            assert (await client.call_tool("echo", {"message": "HTTP"})).structured_content == {"result": "HTTP"}

    asyncio.run(asyncio.wait_for(exercise(), 10))


def test_http_configuration_is_forwarded():
    class RecordingServer:
        def __init__(self):
            self.kwargs = None
            self.app = Starlette()

        def streamable_http_app(self, **kwargs):
            self.kwargs = kwargs
            return self.app

    server = RecordingServer()
    assert build_http_app(server) is server.app
    assert server.kwargs.get("streamable_http_path", "/mcp") == "/mcp"
    assert server.kwargs["json_response"] is True
    assert server.kwargs["stateless_http"] is True
