"""Level 11: check bounded graph evidence retrieval and source lookup."""

from copy import deepcopy

import pytest
from langchain_core.documents import Document

from rag_practice import level11_graph_retrieval as retrieval
from rag_practice.level10_knowledge_graph import Triple

pytestmark = pytest.mark.exercise

AB = Triple("A", "LINK", "B", "a.md")
AC = Triple("A", "DIRECT", "C", "c.md")
BC = Triple("B", "LINK", "C", "b.md")
BA = Triple("B", "BACK", "A", "cycle.md")
BD = Triple("B", "LINK", "D", "d.md")
DC = Triple("D", "LINK", "C", "e.md")


def test_paths_preserve_direction_bound_and_order():
    graph = {"A": [AC, AB], "B": [BA, BC], "C": []}
    snapshot = deepcopy(graph)
    assert retrieval.find_paths(graph, " A ", " C ", 1) == [[AC]]
    assert retrieval.find_paths(graph, "A", "C", 3) == [[AC], [AB, BC]]
    assert retrieval.find_paths(graph, "C", "A", 3) == []
    assert graph == snapshot


def test_hop_limit_on_multi_edge_path():
    graph = {"A": [AB], "B": [BC], "C": []}
    assert retrieval.find_paths(graph, "A", "C", 1) == []
    assert retrieval.find_paths(graph, "A", "C", 2) == [[AB, BC]]


def test_source_distinct_edges_produce_distinct_paths():
    alternate = Triple("A", "LINK", "B", "other.md")
    graph = {"A": [AB, alternate], "B": [BC], "C": []}
    assert retrieval.find_paths(graph, "A", "C", 2) == [[AB, BC], [alternate, BC]]


@pytest.mark.parametrize("start,target", [("missing", "C"), ("A", "missing"), ("A", "A")])
def test_no_positive_simple_path(start, target):
    assert retrieval.find_paths({"A": [AB], "B": [BA], "C": []}, start, target) == []


@pytest.mark.parametrize("start,target,hops", [(" ", "C", 2), ("A", " ", 2), ("A", "C", 0), ("A", "C", -1), ("A", "C", 5)])
def test_invalid_path_parameters(start, target, hops):
    with pytest.raises(ValueError):
        retrieval.find_paths({}, start, target, hops)


def test_graph_answer_combines_unique_facts_with_raw_evidence(monkeypatch):
    paths = [[AB, BC], [AB, BD, DC]]
    source_order = ["a.md", "b.md", "d.md", "e.md"]
    documents = {source: Document(page_content=f"Evidence for {source}", metadata={"source": source}) for source in source_order}
    snapshot = deepcopy((paths, documents))
    searches, generations = [], []

    def find_paths(graph, start, target, max_hops=3):
        searches.append((graph, start, target, max_hops))
        return paths

    def generate(question, facts, docs):
        generations.append((question, facts, docs))
        return "A connects to C through the supplied relations."

    monkeypatch.setattr(retrieval, "find_paths", find_paths)
    result = retrieval.answer_graph_question("  How is A connected to C?  ", "A", "C", {}, documents, generate)
    assert searches == [({}, "A", "C", 3)]
    assert generations == [("How is A connected to C?", [AB, BC, BD, DC], [documents[source] for source in source_order])]
    assert result == {"answer": "A connects to C through the supplied relations.", "sources": source_order, "paths": paths}
    assert (paths, documents) == snapshot


def test_no_path_abstains_without_generation(monkeypatch):
    monkeypatch.setattr(retrieval, "find_paths", lambda *_args, **_kwargs: [])

    def forbidden(*args):
        pytest.fail("No path must not generate an answer.")

    assert retrieval.answer_graph_question("question", "A", "C", {}, {}, forbidden) == {
        "answer": "I don't know based on the provided documents.", "sources": [], "paths": [],
    }


def test_missing_support_document_is_an_error(monkeypatch):
    monkeypatch.setattr(retrieval, "find_paths", lambda *_args, **_kwargs: [[AB, BC]])

    def forbidden(*args):
        pytest.fail("Missing evidence must not reach generation.")

    with pytest.raises(KeyError) as caught:
        retrieval.answer_graph_question("question", "A", "C", {}, {"a.md": Document(page_content="A links B", metadata={"source": "a.md"})}, forbidden)
    assert caught.value.args[0] == "b.md"


def test_blank_graph_question_does_not_search(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Blank question must not search or generate.")

    monkeypatch.setattr(retrieval, "find_paths", forbidden)
    with pytest.raises(ValueError):
        retrieval.answer_graph_question(" \n", "A", "C", {}, {}, forbidden)


def test_graph_generator_error_propagates(monkeypatch):
    monkeypatch.setattr(retrieval, "find_paths", lambda *_args, **_kwargs: [[AB]])

    def fail(*args):
        raise OSError("generator unavailable")

    with pytest.raises(OSError, match="generator unavailable"):
        retrieval.answer_graph_question("question", "A", "B", {}, {"a.md": Document(page_content="A links B", metadata={"source": "a.md"})}, fail)
