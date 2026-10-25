# Level 2：有界业务循环

**本级只解决：怎样重复尝试，并以业务条件保证终止？**

完成已有 [level02_retry.py](../exercises/level02_retry.py) 的 build_retry_graph(checker, max_attempts=3)。

- max_attempts 是正整数，否则在构图时抛 ValueError。
- 输入固定为 `{"attempts":0,"done":False}`。
- 第 n 次尝试恰好调用 checker(n) 一次，n 从 1 连续递增。
- 首次 True 时结束，done=True、status=success、attempts 为实际次数。
- 达到上限仍 False 时结束，done=False、status=exhausted、attempts=max_attempts。
- checker 的异常直接传播；同一图可重复执行，不用全局计数器保存每次运行的次数。

```bash
python -m pytest --run-exercises tests/langgraph/test_level02_retry.py -k 'retry or attempt_limit or checker_exception' -q
```

完成标准：能说明循环的不变量和终止条件。框架 recursion_limit 与业务重试上限不同；本级也不同于后面 RetryPolicy 处理一次节点调用中的暂时失败。

下一步：[Level 3](03_state.md)。
