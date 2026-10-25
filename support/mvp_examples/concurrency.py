"""Observe concurrent reviews with sequential stages and isolated context."""

# Adapted from lifan99/utility; provenance is recorded in SOURCES.json.

import asyncio


ROLES = ("Analyst", "Critic", "Judge")


class FakeClient:
    """Teaching model for FakeClient."""
    def __init__(self):
        self.both_started = asyncio.Event()
        self.started = set()
        self.active = 0
        self.peak = 0
        self.calls = []

    async def complete(self, review_id, role, context):

        self.calls.append((review_id, role, dict(context)))
        self.active += 1
        self.peak = max(self.peak, self.active)
        try:
            if role == "Analyst":
                self.started.add(review_id)
                if len(self.started) == 2:
                    self.both_started.set()

                await self.both_started.wait()
            await asyncio.sleep(0)
            return f"{review_id}:{role}"
        finally:
            self.active -= 1


async def review(review_id, client, slots):
    """Execute the stages using the supplied dependency."""
    context = {"original_input": review_id}
    completed = []
    async with slots:
        for role in ROLES:
            output = await client.complete(review_id, role, context)
            completed.append(output)
            context[f"{role.lower()}_output"] = output
    return completed


async def main():
    """Run the offline demonstration and verify its behavior."""
    client = FakeClient()
    slots = asyncio.Semaphore(2)
    tasks = [asyncio.create_task(review(name, client, slots)) for name in ("R1", "R2")]
    try:

        async with asyncio.timeout(5):
            results = await asyncio.gather(*tasks)
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    assert client.peak == 2 and client.active == 0
    for review_id, result in zip(("R1", "R2"), results):
        assert result == [f"{review_id}:{role}" for role in ROLES]
        calls = [call for call in client.calls if call[0] == review_id]
        assert [call[1] for call in calls] == list(ROLES)
        expected = {"original_input": review_id}
        for _, role, context in calls:
            assert context == expected
            expected[f"{role.lower()}_output"] = f"{review_id}:{role}"
        print(f"{review_id}: Analyst -> Critic -> Judge；上下文隔离通过")
    print("同时等待的 fake 调用峰值：2；结束后活动调用数：0")


if __name__ == "__main__":
    asyncio.run(main())
