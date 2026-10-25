# Level 9：有界异步批处理

**本级只解决：怎样同时处理多个输入，并保留顺序和单项失败？**

前置：async/await、异常与 Runnable。完成 [level09_async.py](../level09_async.py) 的 `run_bounded_batch(runnable, inputs, max_concurrency=3)`。

- 实际使用 Runnable 的异步批处理接口，传递 max_concurrency，不使用同步 invoke 或阻塞事件循环的等待。
- max_concurrency 是正整数，否则抛 `ValueError`；空输入也先校验参数。有效空输入返回 `[]`。
- 同时运行的输入项不超过上限；条件允许且上限大于 1 时，应允许多个输入交错执行。
- 返回结果顺序与输入一致，不按完成顺序重排。
- 普通 Exception 作为对应位置的异常对象返回，不导致其他正常项丢失；取消异常不当作普通业务结果吞掉。
- 不修改输入列表，不要求新建 event loop 或在函数内部调用 asyncio.run。

例如输入 `[1,2,3]`，第 2 项抛 OSError，其余返回输入的十倍，结果应是 `[10, OSError实例, 30]`。

```bash
python -m pytest --run-exercises tests/langchain/test_level09_async.py -q
```

测试使用 `asyncio.run` 驱动本地协程，不需要 pytest-asyncio，不通过网络延迟推断并发。完成标准：能解释最大并发数、返回顺序、单项错误和取消的区别。

下一步：[Level 10](10_streaming.md)。
