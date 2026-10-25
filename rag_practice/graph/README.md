# RAG：知识图谱与多跳检索

先用带来源的人工事实建立有向图，再检索有界多跳路径并回溯原文证据。两级独立于工作流分支；这里的节点是实体，边是关系。

| 级别 | 任务 | 代码 |
| --- | --- | --- |
| 1 | [事实与图建模](lessons/01_knowledge_graph.md) | [level01_knowledge_graph.py](exercises/level01_knowledge_graph.py) |
| 2 | [多跳检索与证据回溯](lessons/02_graph_retrieval.md) | [level02_graph_retrieval.py](exercises/level02_graph_retrieval.py) |

前置为字典、集合与有向图。第1级用 dataclass；第2级原文证据用 LangChain Document。样本放在 [data/](data/)，事实文件为 [facts.json](data/facts.json)。人工事实不代表已经完成自动实体抽取。

本路径属于[项目 P4 关系检索方向](../../projects/knowledge-assistant/04_extensions.md)选修。在相同数据与任务上保留词法／向量基线，报告关系查询收益与维护代价；不作为一般知识库服务的必修前置。

```bash
python -m pytest --run-exercises tests/rag/graph -q
```

这是 GraphRAG 局部检索的教学练习，未包括社区摘要、全局检索与完整自动抽取。模型接收到路径仍需验证关系语义，不能凭路径自动推出新事实。返回 [RAG 路径](../README.md)。
