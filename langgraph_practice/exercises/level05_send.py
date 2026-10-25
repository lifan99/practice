"""Level 5: dispatch indexed work dynamically with Send."""

from collections.abc import Callable

from langgraph.graph.state import CompiledStateGraph


def build_map_graph(worker: Callable[[int], int]) -> CompiledStateGraph:
    """Create one worker task per input occurrence and restore input order."""
    raise NotImplementedError("TODO LG-L5: implement build_map_graph")
