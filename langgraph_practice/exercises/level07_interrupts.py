"""Level 7: pause for explicit approval before a simulated action."""

from collections.abc import Callable

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph


def build_approval_graph(
    checkpointer: BaseCheckpointSaver, publish: Callable[[str], str]
) -> CompiledStateGraph:
    """Use interrupt and Command resume to gate one local publish callback."""
    raise NotImplementedError("TODO LG-L7: implement build_approval_graph")
