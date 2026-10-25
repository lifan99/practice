# RAG：LangGraph 工作流

用显式状态和有界循环管理检索过程：检索→评估证据→改写后重试，合格则生成，预算耗尽则拒答。

| 级别 | 任务 | 代码 | 测试 |
| --- | --- | --- | --- |
| 1 | [可纠正检索](lessons/01_corrective.md) | [level01_corrective.py](exercises/level01_corrective.py) | tests/rag/workflows/test_level01_corrective.py |

前置：RAG 问答与评估、LangGraph 分支和循环。此分支使用 LangChain Document/Runnable 与真正的 CompiledStateGraph，需要完整锁定环境。

本路径属于[项目 P4 工作流方向](../../projects/knowledge-assistant/04_extensions.md)选修；先用 P1–P3 建立基线，再比较纠正循环的质量与额外调用。需要跨进程恢复和业务副作用时另完成 [T3](../../curriculum/transfer/03_recovery.md)。

```bash
python -m pytest --run-exercises tests/rag/workflows -q
```

工作流节点是执行步骤，不是知识图谱实体；受控 grader/rewriter 回调只验证数据流、失败分支与终止，不证明模型判断和改写质量。完成标准详见任务。返回 [RAG 路径](../README.md)，知识图谱分支见 [graph/](../graph/README.md)。
