"""Adapter acceptance checks use core contracts, not an extra RAG implementation."""

import pytest
from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

from langchain_practice.exercises.level11_rag_bridge import (
    as_core_chat_model,
    as_core_retriever,
    from_langchain,
    to_langchain,
)
from rag_practice.core.types import Chunk

pytestmark = pytest.mark.exercise


def test_chunk_round_trip_and_metadata_copy():
    chunk = Chunk("id", "中文", "a.md", 2, 4)
    document = to_langchain(chunk)
    assert document.page_content == "中文"
    assert document.metadata == {"chunk_id": "id", "source": "a.md", "start": 2, "end": 4}
    assert from_langchain(document) == chunk
    document.metadata["source"] = "changed"
    assert chunk.source == "a.md"


@pytest.mark.parametrize("metadata", [{}, {"chunk_id": "a", "source": "a.md", "start": 2, "end": 1}])
def test_missing_or_invalid_provenance_rejected(metadata):
    with pytest.raises(ValueError):
        from_langchain(Document(page_content="x", metadata=metadata))


def test_retriever_adapter_uses_invoke_once_and_neutral_score():
    calls = []
    document = Document(page_content="x", metadata={"chunk_id": "a", "source": "a.md", "start": 0, "end": 1})
    def retrieve(q):
        calls.append(q)
        return [document]
    retrieve_core = as_core_retriever(RunnableLambda(retrieve))
    assert calls == []
    hits = retrieve_core("q")
    assert calls == ["q"] and hits[0].score == 0
    assert hits[0].chunk == Chunk("a", "x", "a.md", 0, 1)


def test_chat_adapter_preserves_messages_without_mutation():
    inputs = []
    def respond(messages):
        inputs.extend(messages)
        return AIMessage(content="answer")
    generate = as_core_chat_model(RunnableLambda(respond))
    messages = [{"role": "system", "content": "rules"}, {"role": "user", "content": "q"}]
    assert generate(messages) == "answer"
    assert [(m.type, m.content) for m in inputs] == [("system", "rules"), ("human", "q")]
    assert messages == [{"role": "system", "content": "rules"}, {"role": "user", "content": "q"}]
