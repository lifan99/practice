"""Connect the real handwritten components using deterministic embedding callbacks."""

import pytest

from rag_practice.core.exercises.level02_chunking import paragraph_chunks
from rag_practice.core.exercises.level04_index import build_index, search_index
from rag_practice.core.exercises.level05_bm25 import build_bm25, search_bm25
from rag_practice.core.exercises.level06_pipeline import answer_question
from rag_practice.core.exercises.level07_metrics import evaluate
from rag_practice.core.exercises.level08_hybrid import hybrid_search
from rag_practice.core.types import Document

pytestmark = pytest.mark.exercise


def embedding(text):
    words = text.split()
    return [float(words.count("alpha")), float(words.count("beta"))]


def test_vector_pipeline_preserves_offsets_through_generation():
    chunks = paragraph_chunks(Document("alpha\n\nbeta", "note.md"), 6)
    index = build_index(chunks, lambda texts: [embedding(text) for text in texts])
    calls = []
    def retrieve(question):
        return search_index(question, index, embedding, 1, {"note.md"})
    def generate(messages):
        calls.append(messages)
        assert "[note.md:7:11|note.md]\nbeta" in messages[1]["content"]
        return "supported answer"
    assert answer_question(" beta ", retrieve, generate) == {
        "answer": "supported answer", "sources": ["note.md"], "chunk_ids": ["note.md:7:11"]
    }
    assert len(calls) == 1


def test_bm25_dense_fusion_and_evaluation_share_chunk_labels():
    chunks = paragraph_chunks(Document("alpha\n\nbeta", "note.md"), 6)
    dense_index = build_index(chunks, lambda texts: [embedding(text) for text in texts])
    lexical_index = build_bm25(chunks, str.split)
    def retrieve(question):
        return hybrid_search(
            question,
            lambda q: search_bm25(q, lexical_index, str.split, 1),
            lambda q: search_index(q, dense_index, embedding, 1),
            1,
        )
    assert evaluate([{"question": "beta", "relevance": {"note.md:7:11": 3}}], retrieve, 1) == {
        "recall": 1.0, "mrr": 1.0, "ndcg": 1.0
    }
