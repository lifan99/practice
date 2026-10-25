"""Real SDK round trips against the provided non-exercise server."""

import asyncio

from mcp import Client

from mcp_practice.support.reference_server import create_reference_server
from mcp_practice.support.transports import client_for_app


def test_mcp_in_memory_runtime():
    async def exercise():
        async with Client(create_reference_server(), read_timeout_seconds=3) as client:
            assert [tool.name for tool in (await client.list_tools()).tools] == ["echo"]
            assert (await client.call_tool("echo", {"message": "ready"})).structured_content == {"result": "ready"}
            assert (await client.read_resource("health://ready")).contents[0].text == "ready"

    asyncio.run(asyncio.wait_for(exercise(), 10))


def test_mcp_http_runtime_without_socket():
    async def exercise():
        app = create_reference_server().streamable_http_app(json_response=True, stateless_http=True)
        async with client_for_app(app) as client:
            assert (await client.call_tool("echo", {"message": "HTTP ready"})).structured_content == {"result": "HTTP ready"}

    asyncio.run(asyncio.wait_for(exercise(), 10))
