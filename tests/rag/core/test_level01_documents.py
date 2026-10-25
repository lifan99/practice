"""Core 1: file boundaries, source identity, and deterministic order."""

import pytest

from rag_practice.core.exercises.level01_documents import load_documents
from rag_practice.core.types import Document

pytestmark = pytest.mark.exercise


def test_preserves_original_text_and_reads_only_current_markdown_files(tmp_path):
    (tmp_path / "b.md").write_text("  中文\n", encoding="utf-8")
    (tmp_path / "a.md").write_text("first", encoding="utf-8")
    (tmp_path / "blank.md").write_text(" \n", encoding="utf-8")
    (tmp_path / "ignore.MD").write_text("ignored", encoding="utf-8")
    (tmp_path / "folder.md").mkdir()
    (tmp_path / "folder.md" / "nested.md").write_text("ignored", encoding="utf-8")
    assert load_documents(tmp_path) == [Document("first", "a.md"), Document("  中文\n", "b.md")]


def test_empty_directory(tmp_path):
    assert load_documents(tmp_path) == []


def test_missing_directory(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_documents(tmp_path / "missing")


def test_file_is_not_a_directory(tmp_path):
    path = tmp_path / "file.md"
    path.write_text("x", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        load_documents(path)


def test_invalid_utf8_propagates(tmp_path):
    (tmp_path / "bad.md").write_bytes(b"\xff")
    with pytest.raises(UnicodeDecodeError):
        load_documents(tmp_path)
