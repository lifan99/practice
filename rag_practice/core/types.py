"""Provided data contracts, not exercise implementations."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import TypedDict


@dataclass(frozen=True)
class Document:
    text: str
    source: str


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    text: str
    source: str
    start: int
    end: int


@dataclass(frozen=True)
class SearchHit:
    chunk: Chunk
    score: float


@dataclass(frozen=True)
class VectorIndex:
    chunks: tuple[Chunk, ...]
    vectors: tuple[tuple[float, ...], ...]


@dataclass(frozen=True)
class BM25Index:
    chunks: tuple[Chunk, ...]
    tokens: tuple[tuple[str, ...], ...]
    k1: float = 1.5
    b: float = 0.75


class ChatMessage(TypedDict):
    role: str
    content: str


class Answer(TypedDict):
    answer: str
    sources: list[str]
    chunk_ids: list[str]


class RetrievalCase(TypedDict):
    question: str
    relevance: dict[str, int]


Vector = Sequence[float]
EmbedDocuments = Callable[[list[str]], Sequence[Vector]]
EmbedQuery = Callable[[str], Vector]
Retriever = Callable[[str], list[SearchHit]]
ChatModel = Callable[[list[ChatMessage]], str]
Tokenizer = Callable[[str], list[str]]
