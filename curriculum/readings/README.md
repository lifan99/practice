# 基础读物：从 MVP 到知识库项目

这组读物以多 Agent 审核 MVP 为案例，讲解契约校验、异步执行、HTTP 与服务生命周期，并配有可独立运行的示例。先掌握这些通用机制，再将它们迁移到知识库项目。材料来源、版本与改编范围见 [来源说明](SOURCES.md)。

| 读物 | 需要的先修 | 读后运行 | 再进入独立任务 |
| --- | --- | --- | --- |
| [1 契约、校验与依赖](01_contracts.md) | 函数、字典、异常 | protocols.py、quotes.py | [F1](../foundations/01_contracts.md)，RAG C1／C2 |
| [2 异步、超时与取消](02_async.md) | try/finally、上下文管理器 | concurrency.py、timeouts.py、cancellation.py | [F2](../foundations/02_async.md)、[T2](../transfer/02_async.md) |
| [3 HTTP 与模型调用的数据边界](03_http.md) | 字典、字符串与字节 | http_contract.py | [F3](../foundations/03_service.md) 的接口部分、[F4](../foundations/04_models.md) 的调用部分 |
| [4 服务准入与生命周期](04_service.md) | 前三篇 | admission.py | [P2](../../projects/knowledge-assistant/02_service.md) 的容量与关闭部分 |

示例代码统一在 [support/mvp_examples/](../../support/mvp_examples/README.md)。在仓库根目录执行 `python support/mvp_examples/run_all.py`，使用 Python 3.12，只需标准库。讲解可分篇阅读；每篇先观察例子，再解释行为，最后做原有独立任务，避免把阅读过的示例算作独立完成。

## 已补齐与仍需补建的范围

本组已提供上述四个主题的入门讲解、代码阅读顺序、观察方法与项目连接。示例可运行，独立作业规格没有附答案。SQL schema／迁移／事务的系统讲义、容器部署讲义，以及 tokenization／embedding／生成模型原理仍待补建；[F3](../foundations/03_service.md)与[F4](../foundations/04_models.md)目前只对这些部分提供任务与官方资料入口。

MVP 本身没有数据库、持久化身份与历史恢复，不能把其示例通过算作 P2 的存储／权限验收。关系检索和 GraphRAG 也没有从该项目复用。返回[主修路线](../README.md)。
