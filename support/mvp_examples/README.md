# 从审核 MVP 复用的离线示例

示例改编自[多 Agent 审核 MVP](https://github.com/lifan99/utility/tree/51d9f356e2a3c5bf27bff93aff2a7cf523a87232)，用于观察依赖替换、引用校验、异步执行与服务边界。来源版本和哈希见 [SOURCES.json](SOURCES.json)。这些是配套讲解示例，独立作业仍由学习者完成。

在仓库根目录使用 Python 3.12，无需安装 MVP、模型 Key、FastAPI 或其他第三方依赖：

```bash
python support/mvp_examples/run_all.py
python support/mvp_examples/concurrency.py
python support/mvp_examples/cancellation.py
```

统一入口在独立子进程用 `-I -S` 执行每个示例，逐项限时并检查退出状态；请保持断言启用。全部通过说明本地受控示例正常，不表示独立练习、真实 HTTP、模型效果、持久化或项目阶段已经验收。

| 示例 | 阅读时观察什么 | 配套讲解 |
| --- | --- | --- |
| [protocols.py](protocols.py) | 同一业务入口替换 fixed／echo 依赖；Protocol 不负责运行时验证 | [契约与依赖](../../curriculum/readings/01_contracts.md) |
| [quotes.py](quotes.py) | 偏移、bool、重复正文与原文切片 | [契约与依赖](../../curriculum/readings/01_contracts.md) |
| [concurrency.py](concurrency.py) | 审核间交错、审核内顺序、上下文快照 | [异步](../../curriculum/readings/02_async.md) |
| [timeouts.py](timeouts.py) | 单次／总预算、取消清理和无关 TimeoutError | [异步](../../curriculum/readings/02_async.md) |
| [cancellation.py](cancellation.py) | 请求取消后等待退出，名额可复用 | [异步](../../curriculum/readings/02_async.md) |
| [http_contract.py](http_contract.py) | 人工构造成功／失败响应与公开错误映射 | [HTTP](../../curriculum/readings/03_http.md) |
| [admission.py](admission.py) | 单循环的活动标识、容量、拒绝与关闭顺序 | [服务边界](../../curriculum/readings/04_service.md) |

http_contract.py 不发送 HTTP，admission.py 不启动 API 服务。它们的 409／429／502 等是原 MVP 的设计选择；不可直接当作知识库项目的通用协议。示例的活动去重不跨进程，不是持久化幂等；超时示例的短时限仅为观察取消，不是产品性能要求。

原 MVP 的客户端依赖 HTTPX 0.28 系列，课程 MCP 传输使用 httpx2；这里的标准库示例可独立运行。运行原服务时，请使用该项目的独立环境与说明。
