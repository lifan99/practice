"""Exercise 1: build a graph with conditional routing."""

from typing import TypedDict

from langgraph.graph.state import CompiledStateGraph


class RoutingState(TypedDict, total=False):
    question: str
    category: str
    answer: str
    trace: list[str]


def build_graph() -> CompiledStateGraph:
    """Build the normalization, classification, and response workflow."""
    raise NotImplementedError("TODO LG-1: implement build_graph")
