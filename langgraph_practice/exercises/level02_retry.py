"""Exercise 2: implement a bounded retry workflow."""

from collections.abc import Callable
from typing import TypedDict

from langgraph.graph.state import CompiledStateGraph


class RetryState(TypedDict, total=False):
    attempts: int
    done: bool
    status: str


def build_retry_graph(
    checker: Callable[[int], bool], max_attempts: int = 3
) -> CompiledStateGraph:
    """Build a workflow that stops on success or at the attempt limit."""
    raise NotImplementedError("TODO LG-2: implement build_retry_graph")
