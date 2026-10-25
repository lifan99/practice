"""Public behavior checks for indexing, context forwarding, and recall."""

from copy import deepcopy
from pathlib import Path

import pytest
from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from langchain_core.vectorstores import InMemoryVectorStore

from practice_support import KeywordEmbeddings
from rag_practice.ex01_index import build_index, load_documents, split_documents
from rag_practice.ex02_qa import answer_question, recall_at_k

pytestmark = pytest.mark.exercise


def test_loading_order_content_and_sources(tmp_path):
    (tmp_path / "b.md").write_text("  graph  ", encoding="utf-8")
    (tmp_path / "a.md").write_text("prompt 模板", encoding="utf-8")
    (tmp_path / "empty.md").write_text(" \n", encoding="utf-8")
    (tmp_path / "ignore.txt").write_text("ignore", encoding="utf-8")
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "c.md").write_text("ignore", encoding="utf-8")
    docs = load_documents(tmp_path)
    assert [doc.page_content for doc in docs] == ["prompt 模板", "graph"]
    assert [doc.metadata["source"] for doc in docs] == ["a.md", "b.md"]


def test_missing_directory(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_documents(tmp_path / "missing")


def test_file_is_not_directory(tmp_path):
    path = tmp_path / "file.md"
    path.write_text("content", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        load_documents(path)


def test_empty_directory(tmp_path):
    assert load_documents(tmp_path) == []


def test_splitting_preserves_metadata_and_character_limit():
    doc = Document(page_content="abcdefghij" * 20, metadata={"source": "a.md", "tag": "test"})
    snapshot = deepcopy(doc)
    chunks = split_documents([doc], chunk_size=40, chunk_overlap=5)
    assert len(chunks) > 1
    assert all(0 < len(chunk.page_content) <= 40 for chunk in chunks)
    assert all(chunk.metadata == doc.metadata for chunk in chunks)
    assert chunks[0].page_content.startswith("abcdefghij")
    assert chunks[-1].page_content.endswith("abcdefghij")
    assert doc == snapshot


@pytest.mark.parametrize("size,overlap", [(0, 0), (-1, 0), (40, -1), (40, 40), (40, 41)])
def test_invalid_split_parameters(size, overlap):
    with pytest.raises(ValueError):
        split_documents([], chunk_size=size, chunk_overlap=overlap)


def test_empty_documents_can_be_split():
    assert split_documents([]) == []


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


def test_sample_corpus_can_be_loaded():
    directory = Path(__file__).resolve().parents[1] / "rag_practice" / "data"
    assert len(load_documents(directory)) == 3


def test_answer_forwards_question_context_and_sources():
    docs = [
        Document(page_content="Unique evidence alpha.", metadata={"source": "a.md"}),
        Document(page_content="Unique evidence beta.", metadata={"source": "b.md"}),
        Document(page_content="Unique evidence gamma.", metadata={"source": "a.md"}),
    ]
    snapshot = deepcopy(docs)
    queries, prompts = [], []

    def retrieve(query):
        queries.append(query)
        return docs

    def generate(prompt):
        messages = prompt.to_messages() if hasattr(prompt, "to_messages") else prompt
        prompts.append(messages)
        return AIMessage(content="A grounded answer.")

    result = answer_question("  What is supported?  ", RunnableLambda(retrieve), RunnableLambda(generate))
    assert result == {"answer": "A grounded answer.", "sources": ["a.md", "b.md"]}
    assert queries == ["What is supported?"]
    assert len(prompts) == 1
    assert any(message.type == "system" and message.content.strip() for message in prompts[0])
    content = "\n".join(str(message.content) for message in prompts[0])
    assert "What is supported?" in content
    for doc in docs:
        assert doc.page_content in content
        assert doc.metadata["source"] in content
    assert docs == snapshot


def test_no_hits_does_not_call_model():
    queries = []

    def retrieve(query):
        queries.append(query)
        return []

    def forbidden(_):
        pytest.fail("The model must not run without retrieved documents.")

    result = answer_question("unknown", RunnableLambda(retrieve), RunnableLambda(forbidden))
    assert result == {"answer": "I don't know based on the provided documents.", "sources": []}
    assert queries == ["unknown"]


def test_blank_question_does_not_call_dependencies():
    def forbidden(_):
        pytest.fail("Dependencies must not run for blank input.")

    with pytest.raises(ValueError):
        answer_question(" \n", RunnableLambda(forbidden), RunnableLambda(forbidden))


@pytest.mark.parametrize("retrieved,relevant,k,expected", [
    (["a", "a", "b"], {"a", "b"}, 2, 0.5),
    (["a", "a", "b"], {"a", "b"}, 3, 1.0),
    (["x", "a"], {"a", "b"}, 1, 0.0),
    (["a"], {"a", "b"}, 10, 0.5),
    ([], {"a"}, 3, 0.0),
])
def test_source_recall(retrieved, relevant, k, expected):
    assert recall_at_k(retrieved, relevant, k) == pytest.approx(expected)


@pytest.mark.parametrize("relevant,k", [({"a"}, 0), ({"a"}, -1), (set(), 1)])
def test_invalid_recall_inputs(relevant, k):
    with pytest.raises(ValueError):
        recall_at_k([], relevant, k)
