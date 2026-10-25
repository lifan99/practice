"""Level 10: distinguish node updates, state snapshots, and interruption."""

from typing import Any, TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph


class NodeUpdate(TypedDict):
    node: str
    values: dict[str, Any]


class RunReport(TypedDict):
    snapshots: list[dict[str, Any]]
    output: Any
    interrupted: bool
    interrupts: list[Any]


def collect_updates(
    graph: CompiledStateGraph, inputs: Any, config: RunnableConfig | None = None
) -> list[NodeUpdate]:
    """Collect ordinary node updates from the unified v2 stream format."""
    raise NotImplementedError("TODO LG-L10A: implement collect_updates")


def observe_run(
    graph: CompiledStateGraph, inputs: Any, config: RunnableConfig | None = None
) -> RunReport:
    """Consume the v3 values projection and preserve output and interrupts."""
    raise NotImplementedError("TODO LG-L10B: implement observe_run")
