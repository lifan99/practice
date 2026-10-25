"""Level 6: check opaque cursors, duplicate names, and bounded discovery."""

import asyncio

import pytest
from mcp_types import ListToolsResult, Tool

from mcp_practice.exercises.level06_pagination import PaginationError, list_all_tools

pytestmark = pytest.mark.exercise


def tool(name):
    return Tool(name=name, input_schema={"type": "object"})


def test_pages_keep_last_page_and_first_duplicate_descriptor():
    first = tool("a")

    class Pages:
        def __init__(self):
            self.cursors = []

        async def list_tools(self, *, cursor=None):
            self.cursors.append(cursor)
            return {None: ListToolsResult(tools=[first], next_cursor=""), "": ListToolsResult(tools=[], next_cursor="opaque/token"), "opaque/token": ListToolsResult(tools=[tool("a"), tool("b")])}[cursor]

    client = Pages()
    result = asyncio.run(list_all_tools(client, 3))
    assert [item.name for item in result] == ["a", "b"]
    assert result[0] is first
    assert client.cursors == [None, "", "opaque/token"]


@pytest.mark.parametrize("repeated", [False, True])
def test_broken_pagination_is_bounded(repeated):
    class Pages:
        def __init__(self):
            self.cursors = []

        async def list_tools(self, *, cursor=None):
            self.cursors.append(cursor)
            return ListToolsResult(tools=[], next_cursor="same" if repeated else str(len(self.cursors)))

    client = Pages()
    with pytest.raises(PaginationError):
        asyncio.run(list_all_tools(client, 3))
    assert len(client.cursors) == (2 if repeated else 3)


@pytest.mark.parametrize("limit", [0, -1])
def test_invalid_page_limit_calls_nothing(limit):
    class Forbidden:
        async def list_tools(self, **kwargs):
            pytest.fail("Invalid limit must not list tools.")

    with pytest.raises(ValueError):
        asyncio.run(list_all_tools(Forbidden(), limit))


def test_empty_final_page():
    class Empty:
        async def list_tools(self, **kwargs):
            return ListToolsResult(tools=[])

    assert asyncio.run(list_all_tools(Empty())) == []
