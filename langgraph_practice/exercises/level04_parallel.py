"""Level 4: fan out independent reviews and join their state updates."""

from collections.abc import Callable

from langgraph.graph.state import CompiledStateGraph


def build_parallel_review(
    reviewers: dict[str, Callable[[str], str]],
) -> CompiledStateGraph:
    """Run named review nodes concurrently and collect one complete report."""
    raise NotImplementedError("TODO LG-L4: implement build_parallel_review")
