"""Core 1: regular files, original text, source identity, and deterministic order."""

import os
from pathlib import Path

import pytest

from rag_practice.core.exercises.level01_documents import load_documents
from rag_practice.core.types import Document

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("directory_name", ["folder.md", "chapter.md"])
def test_preserves_original_text_and_reads_only_current_markdown_files(tmp_path, directory_name):
    (tmp_path / "b.md").write_text("  中文\n", encoding="utf-8")
    (tmp_path / "a.md").write_text("first", encoding="utf-8")
    (tmp_path / "blank.md").write_text(" \n", encoding="utf-8")
    (tmp_path / "ignore.MD").write_text("ignored", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("ignored", encoding="utf-8")
    (tmp_path / "a.md.bak").write_text("ignored", encoding="utf-8")
    (tmp_path / directory_name).mkdir()
    (tmp_path / directory_name / "nested.md").write_text("ignored", encoding="utf-8")
    assert load_documents(tmp_path) == [Document("first", "a.md"), Document("  中文\n", "b.md")]


def test_accepts_regular_file_named_folder_md(tmp_path):
    (tmp_path / "folder.md").write_text("  合法正文\n", encoding="utf-8")
    assert load_documents(tmp_path) == [Document("  合法正文\n", "folder.md")]


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="Named pipes require os.mkfifo")
def test_skips_named_pipe_without_attempting_to_read_it(tmp_path, monkeypatch):
    pipe = tmp_path / "pipe.md"
    try:
        os.mkfifo(pipe)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"Named pipes are unavailable in this filesystem: {exc}")

    (tmp_path / "regular.md").write_text("正文", encoding="utf-8")
    read_text = Path.read_text

    def guarded_read_text(path, *args, **kwargs):
        if path == pipe:
            pytest.fail("A named pipe must be skipped without attempting a read")
        return read_text(path, *args, **kwargs)

    # Fail before opening the pipe so an incorrect implementation cannot block.
    monkeypatch.setattr(Path, "read_text", guarded_read_text)
    assert load_documents(tmp_path) == [Document("正文", "regular.md")]


def test_directory_with_only_non_markdown_files_returns_empty_list(tmp_path):
    for name in ["note.txt", "note.MD", "note.md.bak"]:
        (tmp_path / name).write_text("not included", encoding="utf-8")
    assert load_documents(tmp_path) == []


@pytest.mark.parametrize("text", ["", " \t\n\n"])
def test_blank_markdown_files_return_empty_list(tmp_path, text):
    (tmp_path / "blank.md").write_text(text, encoding="utf-8")
    assert load_documents(tmp_path) == []


def test_preserves_internal_blank_lines(tmp_path):
    text = "  第一段\n\n\t第二段\n"
    (tmp_path / "paragraphs.md").write_text(text, encoding="utf-8")
    assert load_documents(tmp_path) == [Document(text, "paragraphs.md")]


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
