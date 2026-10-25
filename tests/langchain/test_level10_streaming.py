"""Level 10: check lazy incremental streams and early resource cleanup."""

import asyncio
from copy import deepcopy
from types import SimpleNamespace

import pytest
from langchain_core.messages import AIMessageChunk, HumanMessage

from langchain_practice.level10_streaming import astream_text, stream_text

pytestmark = pytest.mark.exercise


def test_sync_stream_is_lazy_and_preserves_chunk_boundaries():
    events, streams = [], []
    messages = [HumanMessage(content="hello")]
    snapshot = deepcopy(messages)

    def stream(inputs):
        events.append("opened")
        assert inputs == messages

        def chunks():
            try:
                for text in ["", "Hello", " ", "world"]:
                    yield AIMessageChunk(content=text)
            finally:
                events.append("closed")

        result = chunks()
        streams.append(result)
        return result

    iterator = stream_text(SimpleNamespace(stream=stream), messages)
    assert events == []
    assert next(iterator) == "Hello"
    assert events == ["opened"]
    assert list(iterator) == [" ", "world"]
    assert events == ["opened", "closed"]
    assert messages == snapshot


def test_sync_early_close_closes_held_underlying_stream():
    events, held = [], []

    def stream(_):
        def chunks():
            try:
                yield AIMessageChunk(content="first")
                yield AIMessageChunk(content="second")
            finally:
                events.append("closed")

        result = chunks()
        held.append(result)
        return result

    iterator = stream_text(SimpleNamespace(stream=stream), [])
    assert next(iterator) == "first"
    iterator.close()
    assert events == ["closed"]


def test_sync_stream_propagates_partial_failure():
    def stream(_):
        yield AIMessageChunk(content="first")
        raise OSError("stream interrupted")

    iterator = stream_text(SimpleNamespace(stream=stream), [])
    assert next(iterator) == "first"
    with pytest.raises(OSError, match="stream interrupted"):
        next(iterator)


def test_sync_rejects_unsupported_content_blocks():
    model = SimpleNamespace(stream=lambda _: iter([AIMessageChunk(content=[{"type": "text", "text": "block"}])]))
    with pytest.raises(TypeError):
        list(stream_text(model, []))


def test_async_stream_is_lazy_and_incremental():
    async def exercise():
        events, held = [], []

        def astream(_):
            events.append("opened")

            async def chunks():
                try:
                    for text in ["", "Hello", " ", "world"]:
                        await asyncio.sleep(0)
                        yield AIMessageChunk(content=text)
                finally:
                    events.append("closed")

            result = chunks()
            held.append(result)
            return result

        iterator = astream_text(SimpleNamespace(astream=astream), [])
        assert events == []
        assert await anext(iterator) == "Hello"
        assert events == ["opened"]
        assert [part async for part in iterator] == [" ", "world"]
        assert events == ["opened", "closed"]

    asyncio.run(exercise())


def test_async_early_close_closes_held_underlying_stream():
    async def exercise():
        events, held = [], []

        def astream(_):
            async def chunks():
                try:
                    yield AIMessageChunk(content="first")
                    yield AIMessageChunk(content="second")
                finally:
                    events.append("closed")

            result = chunks()
            held.append(result)
            return result

        iterator = astream_text(SimpleNamespace(astream=astream), [])
        assert await anext(iterator) == "first"
        await iterator.aclose()
        assert events == ["closed"]

    asyncio.run(exercise())


def test_async_stream_propagates_partial_failure():
    async def exercise():
        async def astream(_):
            yield AIMessageChunk(content="first")
            raise OSError("stream interrupted")

        iterator = astream_text(SimpleNamespace(astream=astream), [])
        assert await anext(iterator) == "first"
        with pytest.raises(OSError, match="stream interrupted"):
            await anext(iterator)

    asyncio.run(exercise())


def test_async_rejects_unsupported_content_blocks():
    async def exercise():
        async def astream(_):
            yield AIMessageChunk(content=[{"type": "text", "text": "block"}])

        with pytest.raises(TypeError):
            _ = [part async for part in astream_text(SimpleNamespace(astream=astream), [])]

    asyncio.run(exercise())
