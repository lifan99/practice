"""Dependency smoke tests; these do not require exercise implementations."""

from typing import TypedDict

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END, START, StateGraph

from practice_support import KeywordEmbeddings, fake_chat_model


def test_offline_chat_model():
    assert fake_chat_model("ready").invoke("hello").content == "ready"


def test_graph_runtime():
    class State(TypedDict):
        value: str

    builder = StateGraph(State)
    builder.add_node("echo", lambda state: {"value": state["value"]})
    builder.add_edge(START, "echo")
    builder.add_edge("echo", END)
    assert builder.compile().invoke({"value": "ready"}) == {"value": "ready"}


def test_vector_store_and_splitter():
    docs = [Document(page_content="langgraph graph checkpoint", metadata={"source": "a"})]
    chunks = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0).split_documents(docs)
    store = InMemoryVectorStore(embedding=KeywordEmbeddings())
    store.add_documents(chunks)
    assert store.as_retriever(search_kwargs={"k": 1}).invoke("checkpoint")[0].metadata["source"] == "a"
