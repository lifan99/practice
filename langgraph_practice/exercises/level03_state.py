"""Level 3: merge identified messages and use a reducer-backed graph."""

from collections.abc import Callable

from langchain_core.messages import AIMessage, BaseMessage
from langgraph.graph.state import CompiledStateGraph


def merge_messages(
    existing: list[BaseMessage], updates: list[BaseMessage]
) -> list[BaseMessage]:
    """Apply native ID-aware message updates without mutating input objects."""
    raise NotImplementedError("TODO LG-L3A: implement merge_messages")


def build_message_graph(
    responder: Callable[[list[BaseMessage]], AIMessage],
) -> CompiledStateGraph:
    """Append or replace a responder message through a state reducer."""
    raise NotImplementedError("TODO LG-L3B: implement build_message_graph")
