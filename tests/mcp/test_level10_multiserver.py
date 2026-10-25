"""Level 10: check connection unwinding and unambiguous tool routing."""

import asyncio

import pytest
from mcp_types import Tool

from mcp_practice import level10_multiserver as multi

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("failure", [None, "connect", "body"])
def test_named_clients_unwind_in_reverse_order(monkeypatch, failure):
    events = []

    class ClientStub:
        def __init__(self, config):
            self.config = config

        async def __aenter__(self):
            events.append(f"open:{self.config}")
            if failure == "connect" and self.config == "second":
                raise OSError("connect unavailable")
            return self

        async def __aexit__(self, *args):
            events.append(f"close:{self.config}")

    monkeypatch.setattr(multi, "Client", ClientStub)

    async def exercise():
        async with multi.connect_servers({"alpha": "first", "beta": "second"}) as clients:
            assert set(clients) == {"alpha", "beta"}
            assert clients["alpha"].config == "first" and clients["beta"].config == "second"
            if failure == "body":
                raise OSError("body unavailable")

    if failure:
        with pytest.raises(OSError, match="unavailable"):
            asyncio.run(exercise())
    else:
        asyncio.run(exercise())
    expected = ["open:first", "open:second"] + (["close:first"] if failure == "connect" else ["close:second", "close:first"])
    assert events == expected


@pytest.mark.parametrize("alias", ["", " bad", "a__b", "9server"])
def test_invalid_alias_validated_before_any_client(monkeypatch, alias):
    def forbidden(*args, **kwargs):
        pytest.fail("All aliases must be validated before creating clients.")

    monkeypatch.setattr(multi, "Client", forbidden)

    async def exercise():
        async with multi.connect_servers({"good": "first", alias: "second"}):
            pass

    with pytest.raises(ValueError):
        asyncio.run(exercise())


def test_namespace_preserves_remote_routing_and_deep_copies_schema():
    descriptor = Tool(name="search__docs", input_schema={"type": "object", "properties": {"query": {"type": "string"}}})
    bindings = multi.namespace_tools({"beta": [descriptor], "alpha": [descriptor]})
    assert [binding.public_name for binding in bindings] == ["alpha__search__docs", "beta__search__docs"]
    assert [(binding.server, binding.remote_name, binding.description) for binding in bindings] == [("alpha", "search__docs", ""), ("beta", "search__docs", "")]
    bindings[0].input_schema["properties"]["query"]["type"] = "integer"
    assert descriptor.input_schema["properties"]["query"]["type"] == "string"
    assert bindings[1].input_schema["properties"]["query"]["type"] == "string"


def test_namespace_rejects_duplicate_remote_names():
    descriptor = Tool(name="echo", input_schema={"type": "object"})
    with pytest.raises(ValueError):
        multi.namespace_tools({"alpha": [descriptor, descriptor]})


def test_empty_multiserver_scope():
    async def exercise():
        async with multi.connect_servers({}) as clients:
            assert clients == {}

    asyncio.run(exercise())
    assert multi.namespace_tools({}) == []
