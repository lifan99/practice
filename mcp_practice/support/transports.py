"""Provided in-process HTTP fixture; no socket or remote service is opened."""

from contextlib import asynccontextmanager

import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client
from starlette.applications import Starlette


@asynccontextmanager
async def client_for_app(app: Starlette):
    async with app.router.lifespan_context(app):
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app),
            base_url="http://127.0.0.1:8000",
            timeout=10.0,
        ) as http_client:
            transport = streamable_http_client(
                "http://127.0.0.1:8000/mcp", http_client=http_client
            )
            async with Client(transport) as client:
                yield client
