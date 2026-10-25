"""Level 9: check bounded evidence grading and query rewriting."""

from copy import deepcopy

import pytest
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from langgraph.graph.state import CompiledStateGraph

from rag_practice.level09_workflow import build_adaptive_rag

pytestmark = pytest.mark.exercise


def forbidden(*args):
    pytest.fail("This callback must not run on the tested branch.")


def test_direct_success_and_reusable_graph():
    docs = [Document(page_content="evidence", metadata={"source": "a.md"})]
    calls = []

    def grade(question, documents):
        calls.append((question, documents))
        return True

    graph = build_adaptive_rag(RunnableLambda(lambda _: docs), grade, forbidden, lambda *_: "answer", 0)
    assert isinstance(graph, CompiledStateGraph)
    initial = {"question": "  original  "}
    snapshot = deepcopy(initial)
    for _ in range(2):
        result = graph.invoke(initial)
        assert result["question"] == "original"
        assert result["answer"] == "answer"
        assert result["sources"] == ["a.md"]
        assert result["attempts"] == 1 and result["rewrites"] == 0
        assert result["status"] == "success"
        assert result["trace"] == ["initialize", "retrieve", "grade", "generate"]
    assert calls == [("original", docs), ("original", docs)]
    assert initial == snapshot


def test_rewrite_keeps_original_question_and_replaces_evidence():
    stale = [Document(page_content="irrelevant", metadata={"source": "stale.md"})]
    fresh = [Document(page_content="supported", metadata={"source": "good.md"}), Document(page_content="more", metadata={"source": "good.md"})]
    snapshot = deepcopy((stale, fresh))
    queries, rewrites, grades, generations = [], [], [], []

    def retrieve(query):
        queries.append(query)
        return stale if query == "original" else fresh

    def grade(question, documents):
        grades.append((question, documents))
        return documents == fresh

    def rewrite(query):
        rewrites.append(query)
        return "  better query  "

    def generate(question, documents):
        generations.append((question, documents))
        return "supported answer"

    graph = build_adaptive_rag(RunnableLambda(retrieve), grade, rewrite, generate, 1)
    result = graph.invoke({"question": " original "})
    assert queries == ["original", "better query"]
    assert rewrites == ["original"]
    assert grades == [("original", stale), ("original", fresh)]
    assert generations == [("original", fresh)]
    assert result["answer"] == "supported answer"
    assert result["sources"] == ["good.md"]
    assert result["attempts"] == 2 and result["rewrites"] == 1
    assert result["trace"] == ["initialize", "retrieve", "grade", "rewrite", "retrieve", "grade", "generate"]
    assert (stale, fresh) == snapshot


@pytest.mark.parametrize("limit", [0, 2])
def test_rewrite_limit_abstains(limit):
    queries, rewrites = [], []
    rejected = [Document(page_content="irrelevant", metadata={"source": "rejected.md"})]

    def retrieve(query):
        queries.append(query)
        return rejected

    def rewrite(query):
        rewrites.append(query)
        return query + " better"

    graph = build_adaptive_rag(RunnableLambda(retrieve), lambda *_: False, rewrite, forbidden, limit)
    result = graph.invoke({"question": "q"})
    assert len(queries) == limit + 1
    assert len(rewrites) == limit
    assert queries == ["q" + " better" * i for i in range(limit + 1)]
    assert rewrites == queries[:-1]
    assert result["attempts"] == limit + 1 and result["rewrites"] == limit
    assert result["status"] == "abstained"
    assert result["answer"] == "I don't know based on the provided documents."
    assert result["sources"] == []
    assert result["trace"] == ["initialize"] + ["retrieve", "grade", "rewrite"] * limit + ["retrieve", "grade", "abstain"]


def test_empty_evidence_skips_grader():
    graph = build_adaptive_rag(RunnableLambda(lambda _: []), forbidden, forbidden, forbidden, 0)
    assert graph.invoke({"question": "q"})["status"] == "abstained"


def test_blank_question_calls_no_dependencies():
    graph = build_adaptive_rag(RunnableLambda(forbidden), forbidden, forbidden, forbidden)
    with pytest.raises(ValueError):
        graph.invoke({"question": " \n"})


def test_negative_rewrite_limit():
    with pytest.raises(ValueError):
        build_adaptive_rag(RunnableLambda(forbidden), forbidden, forbidden, forbidden, -1)


def test_blank_rewrite_is_invalid():
    graph = build_adaptive_rag(RunnableLambda(lambda _: []), forbidden, lambda _: "  ", forbidden, 1)
    with pytest.raises(ValueError):
        graph.invoke({"question": "q"})


@pytest.mark.parametrize("callback", ["retriever", "grader", "rewriter", "generator"])
def test_callback_error_propagates(callback):
    docs = [Document(page_content="evidence", metadata={"source": "a.md"})]

    def fail(*args):
        raise OSError("callback unavailable")

    graph = build_adaptive_rag(
        RunnableLambda(fail if callback == "retriever" else lambda _: docs),
        fail if callback == "grader" else lambda *_: callback != "rewriter",
        fail if callback == "rewriter" else lambda query: query,
        fail if callback == "generator" else lambda *_: "answer",
        1,
    )
    with pytest.raises(OSError, match="callback unavailable"):
        graph.invoke({"question": "q"})
