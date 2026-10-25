"""Level 1: check file loading and traceable source metadata."""

from pathlib import Path

import pytest
from langchain_core.documents import Document

pytestmark = pytest.mark.exercise

from rag_practice.level01_documents import load_documents


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



def test_sample_corpus_can_be_loaded():
    directory = Path(__file__).resolve().parents[2] / "rag_practice" / "data"
    assert len(load_documents(directory)) == 3

