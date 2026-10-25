"""Level 6: keep graph state per thread using an injected checkpointer."""

from typing import Any

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph


def build_counter_graph(checkpointer: BaseCheckpointSaver) -> CompiledStateGraph:
    """Accumulate deltas in checkpointed thread state."""
    raise NotImplementedError("TODO LG-L6A: implement build_counter_graph")


def counter_snapshot(graph: CompiledStateGraph, thread_id: str) -> dict[str, Any]:
    """Read a thread's checkpoint values without running another node."""
    raise NotImplementedError("TODO LG-L6B: implement counter_snapshot")
