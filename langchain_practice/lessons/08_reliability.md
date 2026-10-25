# Level 8：重试、降级与工具中间件

**本级只解决：不同失败应在哪一层被处理？**

前置：Runnable、异常、Level 6。完成 [level08_reliability.py](../exercises/level08_reliability.py)。

## A：重试后再降级

`build_resilient_chain(primary, fallback, max_attempts=2)` 返回 Runnable，使用原生 `with_retry` 和 `with_fallbacks`。

- max_attempts 是正整数，包含首次调用；小于等于 0 时在构建阶段抛 `ValueError`。
- 只对 primary 的 TimeoutError 重试；达到上限仍超时时调用 fallback 一次。primary 成功后立即返回。
- 其他异常直接传播，不重试、不降级；fallback 的异常也直接传播。
- 重试等待关闭 jitter/backoff，以保持离线测试快速；真实服务的退避策略应另行设计。
- 两路收到原输入，传入的 config 标签和 metadata 应能继续传到实际调用。不要把异常改写成成功文本。

## B：可观察的工具输入失败

`make_tool_error_middleware()` 返回真正的 AgentMiddleware，使用 `wrap_tool_call` 装饰器或实现同名 hook。

- 正常调用 handler(request) 一次，原样返回结果。
- 仅捕获 handler 抛出的 ValueError，返回 ToolMessage：content=`Tool input rejected.`、tool_call_id 与 name 取自 request.tool_call、status=`error`。
- OSError 等其他异常不捕获，不重试 handler。
- 这是同步 hook 练习；不声称已提供异步工具中间件。可以将返回对象传入 Level 6 的 middleware 参数进行实际串联。

```bash
python -m pytest --run-exercises tests/langchain/test_level08_reliability.py -q
```

完成标准：分别解释业务不合法、暂时超时和依赖不可用的处理路径；记录一次重试和一次降级的调用次数，并区分失败 ToolMessage 与成功工具输出。

[官方自定义中间件](https://docs.langchain.com/oss/python/langchain/middleware/custom)。下一步：[Level 9](09_async.md)。
