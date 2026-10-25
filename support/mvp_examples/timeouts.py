"""Distinguish operation and workflow budgets from unrelated timeouts."""

# Adapted from lifan99/utility; provenance is recorded in SOURCES.json.

import asyncio


class ModelTimeout(Exception):
    """Teaching model for ModelTimeout."""
    pass


class ReviewTimeout(Exception):
    """Teaching model for ReviewTimeout."""
    pass


async def limited_call(operation, seconds):
    """Apply an operation budget without reclassifying unrelated timeouts."""
    scope = asyncio.timeout(seconds)
    try:
        async with scope:
            return await operation()
    except TimeoutError as exc:
        if not scope.expired():
            raise
        raise ModelTimeout("model_timeout") from exc


async def review(model_seconds, total_seconds, completed, cleaned):
    """Execute the stages using the supplied dependency."""
    loop = asyncio.get_running_loop()
    deadline = loop.time() + total_seconds
    scope = asyncio.timeout_at(deadline)

    async def analyst():
        await asyncio.sleep(0)
        return "A"

    async def critic():
        """Wait for cancellation and record cleanup."""
        try:
            await asyncio.Event().wait()
        finally:
            cleaned.set()

    try:
        async with scope:
            for operation in (analyst, critic):
                if loop.time() >= deadline:
                    raise ReviewTimeout("total_timeout")
                completed.append(await limited_call(operation, model_seconds))
    except TimeoutError as exc:
        if not scope.expired():
            raise
        raise ReviewTimeout("total_timeout") from exc
    if loop.time() >= deadline:
        raise ReviewTimeout("total_timeout")


async def main():
    """Run the offline demonstration and verify its behavior."""
    cases = [
        (0.02, 5.0, ModelTimeout, "单次模型预算耗尽"),
        (5.0, 0.02, ReviewTimeout, "整次审核预算耗尽"),
    ]
    for model_seconds, total_seconds, expected, label in cases:
        completed = []
        cleaned = asyncio.Event()
        try:
            await review(model_seconds, total_seconds, completed, cleaned)
        except expected as exc:
            assert completed == ["A"]
            assert cleaned.is_set()
            print(f"{label}：{exc}；保留 A；Critic 已清理")
        else:
            raise AssertionError("Expected timeout")


    async def unrelated_timeout():
        raise TimeoutError("unrelated")

    try:
        await limited_call(unrelated_timeout, 5)
    except TimeoutError as exc:
        assert str(exc) == "unrelated"
        print("其他来源的 TimeoutError：未误归类为模型预算耗尽")
    else:
        raise AssertionError("Expected original TimeoutError")


if __name__ == "__main__":
    asyncio.run(main())
