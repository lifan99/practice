"""Level 3: check index construction and retrieval without generation."""

import pytest
from langchain_core.documents import Document

pytestmark = pytest.mark.exercise

from langchain_core.vectorstores import InMemoryVectorStore
from practice_support import KeywordEmbeddings
from rag_practice.level03_retrieval import build_index, search_index


def test_index_retrieves_relevant_source():
    class RecordingEmbeddings(KeywordEmbeddings):
        def __init__(self):
            self.texts = []

        def embed_documents(self, texts):
            self.texts.extend(texts)
            return super().embed_documents(texts)

    embeddings = RecordingEmbeddings()
    docs = [
        Document(page_content="langchain prompt tool", metadata={"source": "lc.md"}),
        Document(page_content="langgraph graph checkpoint", metadata={"source": "lg.md"}),
        Document(page_content="rag retrieval vector", metadata={"source": "rag.md"}),
    ]
    store = build_index(docs, embeddings)
    assert isinstance(store, InMemoryVectorStore)
    assert sorted(embeddings.texts) == sorted(doc.page_content for doc in docs)
    hits = store.as_retriever(search_kwargs={"k": 3}).invoke("langgraph graph checkpoint")
    assert hits[0].metadata["source"] == "lg.md"
    assert {hit.metadata["source"] for hit in hits} == {"lc.md", "lg.md", "rag.md"}
    other = build_index([docs[0]], KeywordEmbeddings())
    assert len(other.similarity_search("prompt", k=10)) == 1
    assert len(store.similarity_search("prompt", k=10)) == 3



def test_empty_index_rejected():
    with pytest.raises(ValueError):
        build_index([], KeywordEmbeddings())


def test_search_uses_normalized_question_and_limit():
    class RecordingIndex(InMemoryVectorStore):
        def __init__(self):
            super().__init__(embedding=KeywordEmbeddings())
            self.calls = []

        def similarity_search(self, query, k=4, **kwargs):
            self.calls.append((query, k))
            return [Document(page_content="evidence", metadata={"source": "a.md"})]

    index = RecordingIndex()
    hits = search_index("  graph checkpoint  ", index, k=1)
    assert index.calls == [("graph checkpoint", 1)]
    assert [hit.metadata["source"] for hit in hits] == ["a.md"]


@pytest.mark.parametrize("question,k", [(" ", 1), ("graph", 0), ("graph", -1)])
def test_invalid_search_does_not_query_index(question, k):
    class ForbiddenIndex(InMemoryVectorStore):
        def similarity_search(self, *args, **kwargs):
            pytest.fail("Invalid input must not query the index.")

    index = ForbiddenIndex(embedding=KeywordEmbeddings())
    with pytest.raises(ValueError):
        search_index(question, index, k)


def test_search_empty_index():
    index = InMemoryVectorStore(embedding=KeywordEmbeddings())
    assert search_index("graph", index, 2) == []


def test_search_retains_duplicate_sources_and_ranking():
    index = InMemoryVectorStore(embedding=KeywordEmbeddings())
    index.add_documents([
        Document(page_content="langgraph graph checkpoint", metadata={"source": "same.md"}),
        Document(page_content="graph", metadata={"source": "same.md"}),
        Document(page_content="rag vector", metadata={"source": "other.md"}),
    ])
    hits = search_index("langgraph graph checkpoint", index, 2)
    assert len(hits) == 2
    assert hits[0].page_content == "langgraph graph checkpoint"
    assert [hit.metadata["source"] for hit in hits] == ["same.md", "same.md"]

