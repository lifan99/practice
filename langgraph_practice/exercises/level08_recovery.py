"""Level 8: distinguish node retry from checkpoint-based failure recovery."""

from collections.abc import Callable

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph


def build_recoverable_graph(
    checkpointer: BaseCheckpointSaver,
    prepare: Callable[[str], str],
    deliver: Callable[[str], str],
    max_attempts: int = 2,
) -> CompiledStateGraph:
    """Retry delivery timeouts and preserve completed preparation on resume."""
    raise NotImplementedError("TODO LG-L8: implement build_recoverable_graph")
