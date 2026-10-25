"""Graph 1: model a directed knowledge graph with evidence provenance."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Triple:
    subject: str
    predicate: str
    object: str
    source: str


KnowledgeGraph = dict[str, list[Triple]]


def build_knowledge_graph(triples: list[Triple]) -> KnowledgeGraph:
    """Normalize facts and build deterministic outgoing adjacency lists."""
    raise NotImplementedError("TODO RAG-G1: implement build_knowledge_graph")
