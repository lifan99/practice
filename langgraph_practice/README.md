# LangGraph 分级练习

使用锁定的 **LangGraph 1.2.17**，共十级：基础分支与循环，逐步进入 reducer、并行、动态任务、checkpoint、人工中断、失败恢复、子图与流式观测。

所有核心函数保留 TODO，不附完整答案；节点使用本地确定性回调，无需模型 API Key。图构建任务必须返回真正的 CompiledStateGraph，不以普通包装器模拟 invoke。

## 学习路径

| 级别 | 本级能力 | 任务 | 代码 |
| --- | --- | --- | --- |
| 1 · 分支 | 状态节点、条件边、执行路径 | [说明](lessons/01_routing.md) | [level01_routing.py](exercises/level01_routing.py) |
| 2 · 业务循环 | 尝试次数、成功与耗尽、终止条件 | [说明](lessons/02_retry.md) | [level02_retry.py](exercises/level02_retry.py) |
| 3 · 状态合并 | reducer、消息 ID、追加/替换/删除 | [说明](lessons/03_state.md) | [level03_state.py](exercises/level03_state.py) |
| 4 · 静态并行 | 独立分支、共享键合并、汇合报告 | [说明](lessons/04_parallel.md) | [level04_parallel.py](exercises/level04_parallel.py) |
| 5 · 动态分发 | Send、任务身份、重复项与归并顺序 | [说明](lessons/05_send.md) | [level05_send.py](exercises/level05_send.py) |
| 6 · Checkpoint | 注入存储、线程隔离、读取 StateSnapshot | [说明](lessons/06_checkpoints.md) | [level06_checkpoints.py](exercises/level06_checkpoints.py) |
| 7 · 人工中断 | interrupt、Command resume、模拟审批 | [说明](lessons/07_interrupts.md) | [level07_interrupts.py](exercises/level07_interrupts.py) |
| 8 · 失败恢复 | RetryPolicy、选择性重试、恢复未完成节点 | [说明](lessons/08_recovery.md) | [level08_recovery.py](exercises/level08_recovery.py) |
| 9 · 子图 | 编译子工作流、父子状态映射、私有字段 | [说明](lessons/09_subgraphs.md) | [level09_subgraphs.py](exercises/level09_subgraphs.py) |
| 10 · 可观测性 | v2 updates、v3 values 投影、完成/暂停/失败 | [说明](lessons/10_observability.md) | [level10_observability.py](exercises/level10_observability.py) |

前置：Python 函数、TypedDict、字典、列表、异常。第 3 级还需要 chat messages；第 4–5 级需要理解合并规则；第 7–8 级依赖 checkpoint；第 9 级强调接口边界；第 10 级观察前面学过的运行行为。

每级包含输入输出、边界情况、独立测试和完成标准。通过测试后，还应能解释状态变化与终止条件。并行任务使用普通回调，不把它们称为已经具备自主规划的多 agent 系统。

## 主修与专题

本主题作为[项目 P4](../projects/knowledge-assistant/04_extensions.md)的工作流选修。优先 Level 1–3、6–8；并行、动态分发、子图与流接口在需要时补相应级别。恢复练习后完成 [T3](../curriculum/transfer/03_recovery.md)，独立验证进程重启和副作用幂等。P2 的基础服务可先交付，不要求引入状态图。

## 如何验收

按[总说明](../README.md)安装依赖，在仓库根目录执行：

```bash
python -m pytest --run-exercises tests/langgraph/test_level01_routing.py -q
python -m pytest --run-exercises tests/langgraph/test_level02_retry.py -q
python -m pytest --run-exercises tests/langgraph -q
```

默认测试跳过全部学生练习，验证提供的运行环境。使用 --run-exercises 才执行验收，初始 NotImplementedError 表示该任务尚未实现。

## 验收实际检查什么

- 消息题检查真正的 ID 替换、RemoveMessage 删除和输入对象保护。
- 静态并行题用同步屏障验证并发；动态分发题保留重复输入的位置，不假设任务完成顺序。
- Checkpoint、暂停与恢复使用真实 InMemorySaver 和框架 API；模拟动作只记录本地调用，不触发外部操作。
- RetryPolicy 题区分暂时超时和普通依赖失败，验证 prepare 已完成后不因恢复而重跑。
- 子图题用独立编译的子图隔离父图适配逻辑，不要求同时完成两份实现才能定位当前问题。
- [runtime_fixtures.py](support/runtime_fixtures.py) 是提供好的纯本地图，用于验证流接口；它不包含学生练习的实现。

InMemorySaver 不保证跨进程持久化；checkpoint 也不自动使真实外部副作用 exactly-once。第 2 级业务循环上限、第 8 级节点重试预算、框架 recursion_limit 是三个不同控制层。

## 流接口版本

第 10 级对照 v2 的统一 stream part 与 v3 的 typed projection。锁定版本将 v3 标为实验性，环境检查可能显示 BetaWarning；它不是 Python SDK 主版本号，也不代表练习失败。stream.values、stream.output 和 stream.interrupts 是不同观察结果，不能用有无 token 判断图是否成功完成。

## 和其他主题衔接

需要模型和 tools 时，可接入 [LangChain](../langchain_practice/README.md) 组件；检索纠正流程可接 [RAG 纠正检索](../rag_practice/workflows/lessons/01_corrective.md)；节点调用外部能力时可接 [MCP](../mcp_practice/README.md) 适配器。本路径的工作流图与 GraphRAG 的实体关系图不同。

## 后续项目

[T3](../curriculum/transfer/03_recovery.md)与[P4 工作流方向](../projects/knowledge-assistant/04_extensions.md)提供了持久化与进程重启的独立任务规格，需自行选择兼容依赖、实现与测试。store 跨线程记忆、time travel、Functional API durable tasks、缓存与异步流、supervisor/handoff、多模型图和观测平台仍为按需专题，不把新增组件数当作能力等级。

## 官方参考

- [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [Subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)
- [Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)
