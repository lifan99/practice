"""Check orchestration with generation replaced by a recording function."""

from copy import deepcopy

import pytest
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda

from rag_practice import level04_generation
from rag_practice.level05_pipeline import answer_question

pytestmark = pytest.mark.exercise


def test_pipeline_reuses_generation_and_deduplicates_sources(monkeypatch):
    docs = [
        Document(page_content="Alpha.", metadata={"source": "a.md"}),
        Document(page_content="Beta.", metadata={"source": "b.md"}),
        Document(page_content="Gamma.", metadata={"source": "a.md"}),
    ]
    snapshot = deepcopy(docs)
    queries, generations = [], []
    model = RunnableLambda(lambda _: pytest.fail("Call the level 4 generator instead."))

    def retrieve(query):
        queries.append(query)
        return docs

    def generate(question, documents, injected_model):
        generations.append((question, documents, injected_model))
        return "A grounded answer."

    monkeypatch.setattr(level04_generation, "generate_answer", generate)
    result = answer_question("  question  ", RunnableLambda(retrieve), model)
    assert result == {"answer": "A grounded answer.", "sources": ["a.md", "b.md"]}
    assert queries == ["question"]
    assert len(generations) == 1
    assert generations[0][0] == "question"
    assert generations[0][1] == docs
    assert generations[0][2] is model
    assert docs == snapshot


def test_no_hits_does_not_generate(monkeypatch):
    queries = []

    def retrieve(question):
        queries.append(question)
        return []

    def forbidden(*args):
        pytest.fail("Empty evidence must not reach generation.")

    monkeypatch.setattr(level04_generation, "generate_answer", forbidden)
    result = answer_question("unknown", RunnableLambda(retrieve), RunnableLambda(forbidden))
    assert result == {"answer": "I don't know based on the provided documents.", "sources": []}
    assert queries == ["unknown"]


def test_blank_question_does_not_call_dependencies(monkeypatch):
    def forbidden(*args):
        pytest.fail("Blank input must not call dependencies.")

    monkeypatch.setattr(level04_generation, "generate_answer", forbidden)
    with pytest.raises(ValueError):
        answer_question(" \n", RunnableLambda(forbidden), RunnableLambda(forbidden))


def test_retrieval_failure_propagates():
    def fail(_):
        raise OSError("retriever unavailable")

    with pytest.raises(OSError, match="retriever unavailable"):
        answer_question("question", RunnableLambda(fail), RunnableLambda(lambda _: "unused"))


def test_generation_failure_propagates(monkeypatch):
    def fail(*args):
        raise OSError("generation unavailable")

    monkeypatch.setattr(level04_generation, "generate_answer", fail)
    docs = [Document(page_content="evidence", metadata={"source": "a.md"})]
    with pytest.raises(OSError, match="generation unavailable"):
        answer_question("question", RunnableLambda(lambda _: docs), RunnableLambda(lambda _: "unused"))
