"""Level 9: check concurrency bounds, result order, and error isolation."""

import asyncio

import pytest
from langchain_core.runnables import RunnableLambda

from langchain_practice.exercises.level09_async import run_bounded_batch

pytestmark = pytest.mark.exercise


def forbidden(_):
    pytest.fail("Asynchronous practice must not call synchronous invoke.")


def test_bounded_batch_overlaps_work_and_preserves_positions():
    async def exercise():
        active = peak = 0
        error = OSError("item unavailable")

        async def work(value):
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            try:
                await asyncio.sleep(0)
                if value == 2:
                    raise error
                return value * 10
            finally:
                active -= 1

        inputs = [1, 2, 3, 4]
        results = await run_bounded_batch(RunnableLambda(forbidden, afunc=work), inputs, 2)
        assert results[0] == 10 and results[1] is error and results[2:] == [30, 40]
        assert peak == 2 and active == 0
        assert inputs == [1, 2, 3, 4]

    asyncio.run(exercise())


def test_empty_async_batch():
    assert asyncio.run(run_bounded_batch(RunnableLambda(forbidden), [], 1)) == []


@pytest.mark.parametrize("concurrency", [0, -1])
def test_invalid_concurrency(concurrency):
    with pytest.raises(ValueError):
        asyncio.run(run_bounded_batch(RunnableLambda(forbidden), [], concurrency))


def test_cancellation_is_not_returned_as_an_ordinary_result():
    async def cancelled(_):
        raise asyncio.CancelledError()

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(run_bounded_batch(RunnableLambda(forbidden, afunc=cancelled), [1], 1))
