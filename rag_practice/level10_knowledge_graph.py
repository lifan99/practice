"""Level 10: model a directed knowledge graph with evidence provenance."""

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
    raise NotImplementedError("TODO RAG-L10: implement build_knowledge_graph")
