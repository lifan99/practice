"""Core 2: exact offsets, overlap termination, and paragraph boundaries."""

import pytest

from rag_practice.core.level02_chunking import paragraph_chunks, window_chunks
from rag_practice.core.types import Chunk, Document

pytestmark = pytest.mark.exercise


@pytest.mark.parametrize("text,size,overlap,spans", [
    ("abcdefghij", 4, 1, [(0, 4), (3, 7), (6, 10)]),
    ("abcdef", 4, 1, [(0, 4), (3, 6)]),
    ("中文 测试", 3, 0, [(0, 3), (3, 5)]),
    ("ab", 4, 3, [(0, 2)]),
    ("", 4, 0, []),
])
def test_window_offsets_and_ids(text, size, overlap, spans):
    document = Document(text, "x.md")
    assert window_chunks(document, size, overlap) == [
        Chunk(f"x.md:{start}:{end}", text[start:end], "x.md", start, end)
        for start, end in spans
    ]
    assert document.text == text


@pytest.mark.parametrize("size,overlap", [(0, 0), (-1, 0), (3, -1), (3, 3), (3, 4)])
def test_invalid_windows_even_on_empty_input(size, overlap):
    with pytest.raises(ValueError):
        window_chunks(Document("", "x.md"), size, overlap)


def test_paragraph_packing_preserves_separator_and_original_offsets():
    document = Document("  aa\n\nbb\n\ncccccc\n\nz  ", "x.md")
    result = paragraph_chunks(document, 6)
    assert [(c.start, c.end, c.text) for c in result] == [
        (2, 8, "aa\n\nbb"), (10, 16, "cccccc"), (18, 19, "z")
    ]
    assert all(c.chunk_id == f"x.md:{c.start}:{c.end}" for c in result)
    assert all(c.text == document.text[c.start:c.end] for c in result)


def test_long_paragraph_is_split_and_not_merged_with_neighbors():
    document = Document("a\n\n1234567\n\nb", "x.md")
    assert [c.text for c in paragraph_chunks(document, 3)] == ["a", "123", "456", "7", "b"]


@pytest.mark.parametrize("text", ["", " \n\n\t "])
def test_blank_paragraph_input(text):
    assert paragraph_chunks(Document(text, "x.md"), 5) == []


def test_invalid_paragraph_budget():
    with pytest.raises(ValueError):
        paragraph_chunks(Document("x", "x.md"), 0)
