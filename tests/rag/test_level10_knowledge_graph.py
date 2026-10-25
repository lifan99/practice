"""Level 10: check graph direction, normalized facts, and provenance."""

from copy import deepcopy
from dataclasses import replace

import pytest

from rag_practice.level10_knowledge_graph import Triple, build_knowledge_graph

pytestmark = pytest.mark.exercise


def test_graph_normalizes_deduplicates_and_sorts():
    triples = [
        Triple(" Alice ", " WORKS_ON ", " Atlas ", " team.md "),
        Triple("Bob", "REVIEWS", "Atlas", "team.md"),
        Triple("Alice", "WORKS_ON", "Atlas", "other.md"),
        Triple("Alice", "WORKS_ON", "Atlas", "team.md"),
    ]
    snapshot = deepcopy(triples)
    graph = build_knowledge_graph(triples)
    assert list(graph) == ["Alice", "Atlas", "Bob"]
    assert graph["Alice"] == [Triple("Alice", "WORKS_ON", "Atlas", "other.md"), Triple("Alice", "WORKS_ON", "Atlas", "team.md")]
    assert graph["Atlas"] == []
    assert graph["Bob"] == [Triple("Bob", "REVIEWS", "Atlas", "team.md")]
    assert triples == snapshot


def test_graph_retains_case_and_self_loops():
    loop = Triple("Alice", "MENTIONS", "Alice", "a.md")
    edge = Triple("alice", "MENTIONS", "Alice", "a.md")
    graph = build_knowledge_graph([loop, edge, loop])
    assert list(graph) == ["Alice", "alice"]
    assert graph["Alice"] == [loop]
    assert graph["alice"] == [edge]


@pytest.mark.parametrize("field", ["subject", "predicate", "object", "source"])
def test_blank_fact_field_invalid(field):
    triple = replace(Triple("A", "LINK", "B", "a.md"), **{field: " \n"})
    with pytest.raises(ValueError):
        build_knowledge_graph([triple])


def test_empty_graph():
    assert build_knowledge_graph([]) == {}
