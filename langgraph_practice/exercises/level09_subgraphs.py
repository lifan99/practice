"""Level 9: compose graphs through explicit parent-child state mappings."""

from langgraph.graph.state import CompiledStateGraph


def build_normalizer_subgraph() -> CompiledStateGraph:
    """Clean raw text and count whitespace-separated words in private state."""
    raise NotImplementedError("TODO LG-L9A: implement build_normalizer_subgraph")


def build_report_graph(normalizer: CompiledStateGraph) -> CompiledStateGraph:
    """Map document input to a supplied subgraph and keep its private keys local."""
    raise NotImplementedError("TODO LG-L9B: implement build_report_graph")
