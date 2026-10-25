"""Core 6: plain message contracts, abstention, and dependency boundaries."""

import pytest

from rag_practice.core import level06_pipeline as module

pytestmark = pytest.mark.exercise


def test_context_format(chunk):
    assert module.format_context([chunk("x", "alpha", "one.md"), chunk("y", "beta", "two.md")]) == (
        "[x|one.md]\nalpha\n\n[y|two.md]\nbeta"
    )
    assert module.format_context([]) == ""


def test_pipeline_invokes_plain_functions_once_and_preserves_chunk_identity(hit, monkeypatch):
    calls = []
    hits = [hit("a"), hit("b"), hit("a"), hit("c", source="b.md")]
    def retrieve(question):
        calls.append(("retrieve", question))
        return hits
    def format_context(chunks):
        assert [c.chunk_id for c in chunks] == ["a", "b", "c"]
        return "FORMATTED EVIDENCE"
    monkeypatch.setattr(module, "format_context", format_context)
    def generate(messages):
        calls.append(("generate", messages))
        assert [m["role"] for m in messages] == ["system", "user"]
        assert messages[0]["content"].strip()
        assert "question" in messages[1]["content"]
        assert "FORMATTED EVIDENCE" in messages[1]["content"]
        return "answer"
    assert module.answer_question("  question  ", retrieve, generate) == {
        "answer": "answer", "sources": ["a.md", "b.md"], "chunk_ids": ["a", "b", "c"]
    }
    assert calls[0] == ("retrieve", "question") and len(calls) == 2
    assert len(hits) == 4


def test_empty_evidence_abstains_without_model_call():
    def forbidden(_):
        pytest.fail("No evidence must not call the model.")
    assert module.answer_question("q", lambda _: [], forbidden) == {
        "answer": "未找到足够的证据。", "sources": [], "chunk_ids": []
    }


def test_invalid_question_before_dependencies():
    def forbidden(_):
        pytest.fail("Invalid question must not call dependencies.")
    with pytest.raises(ValueError):
        module.answer_question(" \n", forbidden, forbidden)


def test_dependency_errors_propagate(hit, monkeypatch):
    monkeypatch.setattr(module, "format_context", lambda _: "context")
    def fail(_):
        raise OSError("unavailable")
    with pytest.raises(OSError, match="unavailable"):
        module.answer_question("q", fail, fail)
    with pytest.raises(OSError, match="unavailable"):
        module.answer_question("q", lambda _: [hit()], fail)
