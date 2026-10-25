"""Core 2: exact source spans, window termination, and paragraph budgets."""

import pytest

from rag_practice.core.exercises.level02_chunking import paragraph_chunks, window_chunks
from rag_practice.core.types import Chunk, Document

pytestmark = pytest.mark.exercise


def assert_exact_chunks(document, chunks, spans):
    """Compare full public values against explicit expected source intervals."""
    assert chunks == [
        Chunk(
            f"{document.source}:{start}:{end}",
            document.text[start:end],
            document.source,
            start,
            end,
        )
        for start, end in spans
    ]


@pytest.mark.parametrize(
    "text,size,overlap,spans",
    [
        pytest.param("abcdefghij", 4, 1, [(0, 4), (3, 7), (6, 10)], id="overlapping"),
        pytest.param("abcdef", 4, 1, [(0, 4), (3, 6)], id="short-tail"),
        pytest.param("abcd", 4, 1, [(0, 4)], id="exact-size"),
        pytest.param("ab", 4, 3, [(0, 2)], id="short-text-large-overlap"),
        pytest.param("abcdefgh", 4, 0, [(0, 4), (4, 8)], id="no-overlap-exact"),
        pytest.param("abcdefghi", 4, 0, [(0, 4), (4, 8), (8, 9)], id="no-overlap-tail"),
        pytest.param("abcde", 3, 2, [(0, 3), (1, 4), (2, 5)], id="maximum-overlap"),
        pytest.param("abc", 1, 0, [(0, 1), (1, 2), (2, 3)], id="unit-size"),
        pytest.param("中文 测试", 3, 0, [(0, 3), (3, 5)], id="chinese"),
        pytest.param("A😀中B", 2, 1, [(0, 2), (1, 3), (2, 4)], id="unicode-code-points"),
        pytest.param(" \t\n", 2, 0, [(0, 2), (2, 3)], id="blank-text-is-preserved"),
        pytest.param(" a\nb ", 3, 0, [(0, 3), (3, 5)], id="edge-and-internal-whitespace"),
        pytest.param("aaaaa", 3, 1, [(0, 3), (2, 5)], id="repeated-text-distinct-spans"),
        pytest.param("", 4, 1, [], id="empty"),
    ],
)
def test_window_offsets_and_ids(text, size, overlap, spans):
    document = Document(text, "资料.v2.md")
    chunks = window_chunks(document, size, overlap)
    assert_exact_chunks(document, chunks, spans)
    assert document == Document(text, "资料.v2.md")


def test_window_default_overlap_is_zero():
    document = Document("abcdef", "default.md")
    assert_exact_chunks(document, window_chunks(document, 4), [(0, 4), (4, 6)])


@pytest.mark.parametrize("text", ["", "abc"], ids=["empty", "nonempty"])
@pytest.mark.parametrize("size,overlap", [(0, 0), (-1, 0), (3, -1), (3, 3), (3, 4)])
def test_invalid_windows_validate_before_processing(text, size, overlap):
    with pytest.raises(ValueError):
        window_chunks(Document(text, "invalid.md"), size, overlap)


def test_window_calls_preserve_independent_results():
    first = Document("aaaaa", "first.md")
    second = Document("XYZ", "second.md")
    first_result = window_chunks(first, 3, 1)
    second_result = window_chunks(second, 2, 0)
    assert_exact_chunks(first, first_result, [(0, 3), (2, 5)])
    assert_exact_chunks(second, second_result, [(0, 2), (2, 3)])
    assert window_chunks(first, 3, 1) == first_result


@pytest.mark.parametrize(
    "text,max_chars,spans",
    [
        pytest.param(
            "  aa\n\nbb\n\ncccccc\n\nz  ", 6,
            [(2, 8), (10, 16), (18, 19)], id="packing-and-original-offsets",
        ),
        pytest.param("", 5, [], id="empty"),
        pytest.param(" \n\n\t ", 5, [], id="blank-only"),
        pytest.param(" \t中文 \n", 4, [(2, 4)], id="trim-paragraph-edges"),
        pytest.param("abcd", 4, [(0, 4)], id="exact-budget"),
        pytest.param("ab\n\nc", 1, [(0, 1), (1, 2), (4, 5)], id="unit-budget"),
        pytest.param("aa\n\nbb", 6, [(0, 6)], id="separator-exact-fit"),
        pytest.param("aa\n\nbb", 5, [(0, 2), (4, 6)], id="separator-exceeds-budget"),
        pytest.param("a\n\nb\n\nc", 4, [(0, 4), (6, 7)], id="greedy-in-order"),
        pytest.param("a\n\nb\n\nc", 7, [(0, 7)], id="all-paragraphs-fit"),
        pytest.param("aa\nbb", 5, [(0, 5)], id="single-newline-is-not-a-separator"),
        pytest.param("aa\nbb", 3, [(0, 3), (3, 5)], id="keep-newline-in-long-paragraph"),
        pytest.param("a\n \t\nb", 6, [(0, 6)], id="spaces-and-tabs-in-separator"),
        pytest.param("a\n\n\n\nb", 6, [(0, 6)], id="repeated-empty-paragraphs-fit"),
        pytest.param("a\n\n\n\nb", 5, [(0, 1), (5, 6)], id="full-gap-counts-in-budget"),
        pytest.param("\n\n a \n\n b \n\n", 5, [(3, 4), (8, 9)], id="outer-and-paragraph-whitespace"),
        pytest.param(
            "a\n\n12345\n\nb", 4, [(0, 1), (3, 7), (7, 8), (10, 11)],
            id="long-tail-must-not-merge-even-when-it-fits",
        ),
        pytest.param(
            "a\n\n123456\n\nb", 3, [(0, 1), (3, 6), (6, 9), (11, 12)],
            id="long-paragraph-exact-multiple",
        ),
        pytest.param("aa\n\naa\n\naa", 3, [(0, 2), (4, 6), (8, 10)], id="repeated-paragraph-offsets"),
        pytest.param("  abcdefg  ", 3, [(2, 5), (5, 8), (8, 9)], id="long-paragraph-nonzero-origin"),
        pytest.param("\u3000a\u3000\n\n\tb\t", 6, [(1, 7)], id="keep-internal-unicode-whitespace"),
        pytest.param(
            "12345\n\nabcde", 3, [(0, 3), (3, 5), (7, 10), (10, 12)],
            id="adjacent-long-paragraphs",
        ),
    ],
)
def test_paragraph_offsets_ids_and_budget(text, max_chars, spans):
    document = Document(text, "段落.md")
    chunks = paragraph_chunks(document, max_chars)
    assert_exact_chunks(document, chunks, spans)
    assert all(0 < len(chunk.text) <= max_chars for chunk in chunks)
    assert document == Document(text, "段落.md")


@pytest.mark.parametrize("text", ["", " \t\n", "x"], ids=["empty", "blank", "nonempty"])
@pytest.mark.parametrize("max_chars", [0, -1])
def test_invalid_paragraph_budget_validates_before_processing(text, max_chars):
    with pytest.raises(ValueError):
        paragraph_chunks(Document(text, "invalid.md"), max_chars)


def test_paragraph_calls_preserve_independent_results():
    first = Document("a\n\nb", "first.md")
    second = Document("XYZ", "second.md")
    first_result = paragraph_chunks(first, 4)
    second_result = paragraph_chunks(second, 2)
    assert_exact_chunks(first, first_result, [(0, 4)])
    assert_exact_chunks(second, second_result, [(0, 2), (2, 3)])
    assert paragraph_chunks(first, 4) == first_result
