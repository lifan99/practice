"""Observe dependency substitution through a structural protocol."""

# Adapted from lifan99/utility; provenance is recorded in SOURCES.json.

from typing import Protocol

class Client(Protocol):
    """Teaching model for Client."""
    def complete(self, *, model: str, messages: list[dict[str, str]]) -> str: ...

class FixedClient:
    """Teaching model for FixedClient."""
    def complete(self, *, model: str, messages: list[dict[str, str]]) -> str:
        return "fixed response"

class EchoClient:
    """Teaching model for EchoClient."""
    def complete(self, *, model: str, messages: list[dict[str, str]]) -> str:
        return messages[0]["content"]

def review(text: str, client: Client) -> str:
    """Execute the stages using the supplied dependency."""
    return client.complete(
        model="teaching-model",
        messages=[{"role": "user", "content": text}],
    )

assert review("hello", FixedClient()) == "fixed response"
assert review("hello", EchoClient()) == "hello"
print(review("hello", FixedClient()))
print(review("hello", EchoClient()))
