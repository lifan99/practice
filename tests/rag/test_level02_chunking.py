"""Level 2: check fixed windows and recursive document splitting."""

from copy import deepcopy

import pytest
from langchain_core.documents import Document

pytestmark = pytest.mark.exercise

from rag_practice.level02_chunking import fixed_size_chunks, split_documents


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


@pytest.mark.parametrize("text,size,overlap,expected", [
    ("abcdefghij", 4, 1, ["abcd", "defg", "ghij"]),
    ("abcd", 4, 1, ["abcd"]),
    ("abc", 4, 1, ["abc"]),
    ("abcdefgh", 4, 0, ["abcd", "efgh"]),
    ("abcdefghi", 4, 0, ["abcd", "efgh", "i"]),
    ("abcde", 3, 2, ["abc", "bcd", "cde"]),
    ("中文文档切分", 3, 1, ["中文文", "文档切", "切分"]),
    (" a\nb ", 3, 0, [" a\n", "b "]),
    ("", 4, 1, []),
])
def test_fixed_character_windows(text, size, overlap, expected):
    assert fixed_size_chunks(text, size, overlap) == expected


@pytest.mark.parametrize("size,overlap", [(0, 0), (-1, 0), (4, -1), (4, 4), (4, 5)])
def test_fixed_windows_validate_even_empty_input(size, overlap):
    with pytest.raises(ValueError):
        fixed_size_chunks("", size, overlap)


def test_recursive_splitting_keeps_all_nonblank_characters():
    text = "".join(chr(0x4E00 + i) for i in range(160))
    chunks = split_documents([Document(page_content=text, metadata={"source": "cn.md"})], 40, 5)
    assert all(0 < len(chunk.page_content) <= 40 for chunk in chunks)
    assert set("".join(chunk.page_content for chunk in chunks)) == set(text)
    assert chunks[0].page_content.startswith(text[:10])
    assert chunks[-1].page_content.endswith(text[-10:])


def test_recursive_splitting_does_not_mix_sources_or_emit_blank_chunks():
    docs = [
        Document(page_content="alpha " * 20, metadata={"source": "a.md"}),
        Document(page_content=" \n\t ", metadata={"source": "blank.md"}),
        Document(page_content="beta " * 20, metadata={"source": "b.md"}),
    ]
    chunks = split_documents(docs, 30, 5)
    assert chunks
    assert {chunk.metadata["source"] for chunk in chunks} == {"a.md", "b.md"}
    for chunk in chunks:
        assert chunk.page_content.strip()
        assert len(chunk.page_content) <= 30
        if chunk.metadata["source"] == "a.md":
            assert "beta" not in chunk.page_content
        else:
            assert "alpha" not in chunk.page_content

