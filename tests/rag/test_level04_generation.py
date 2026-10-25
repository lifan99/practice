"""Check generation independently of document loading and retrieval."""

from copy import deepcopy

import pytest
from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

from rag_practice import level04_generation as generation

pytestmark = pytest.mark.exercise


def test_context_format_preserves_order_and_duplicate_sources():
    docs = [
        Document(page_content="Alpha.", metadata={"source": "a.md"}),
        Document(page_content="Beta.", metadata={"source": "b.md"}),
        Document(page_content=" Gamma. ", metadata={"source": "a.md"}),
    ]
    snapshot = deepcopy(docs)
    assert generation.format_context(docs) == "[a.md]\nAlpha.\n\n[b.md]\nBeta.\n\n[a.md]\n Gamma. "
    assert docs == snapshot


def test_empty_context():
    assert generation.format_context([]) == ""


def test_generation_forwards_formatted_evidence(monkeypatch):
    docs = [Document(page_content="Evidence.", metadata={"source": "a.md"})]
    snapshot = deepcopy(docs)
    contexts, prompts = [], []

    def format_context(documents):
        contexts.append(documents)
        return "UNIQUE-CONTEXT-FROM-FORMATTER"

    def generate(prompt):
        messages = prompt.to_messages() if hasattr(prompt, "to_messages") else prompt
        prompts.append(messages)
        return AIMessage(content="A grounded answer.")

    monkeypatch.setattr(generation, "format_context", format_context)
    result = generation.generate_answer("  What is supported?  ", docs, RunnableLambda(generate))
    assert result == "A grounded answer."
    assert len(contexts) == 1 and contexts[0] == docs
    assert len(prompts) == 1
    assert any(message.type == "system" and message.content.strip() for message in prompts[0])
    content = "\n".join(str(message.content) for message in prompts[0])
    assert "What is supported?" in content
    assert "UNIQUE-CONTEXT-FROM-FORMATTER" in content
    assert docs == snapshot


@pytest.mark.parametrize("question,docs", [
    (" \n", [Document(page_content="evidence", metadata={"source": "a.md"})]),
    ("question", []),
])
def test_invalid_generation_does_not_call_model(question, docs):
    def forbidden(_):
        pytest.fail("Invalid input must not call the model.")

    with pytest.raises(ValueError):
        generation.generate_answer(question, docs, RunnableLambda(forbidden))


def test_model_failure_propagates(monkeypatch):
    monkeypatch.setattr(generation, "format_context", lambda _: "[a.md]\nevidence")

    def fail(_):
        raise OSError("model unavailable")

    docs = [Document(page_content="evidence", metadata={"source": "a.md"})]
    with pytest.raises(OSError, match="model unavailable"):
        generation.generate_answer("question", docs, RunnableLambda(fail))
