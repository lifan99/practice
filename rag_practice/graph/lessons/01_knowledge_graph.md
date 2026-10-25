# Level 1：GraphRAG · 建立带来源的知识图谱

**本级只解决：怎样把实体关系建成可查询、可追溯的图？**

前置：Document、字典、集合和有向图。不要求先完成工作流分支；知识图谱与工作流图是两种不同的数据模型。

## 图的数据契约

[level01_knowledge_graph.py](../exercises/level01_knowledge_graph.py) 已提供不可变的 `Triple(subject, predicate, object, source)`。

例如 `Triple("Alice", "WORKS_ON", "Atlas", "team.md")` 表示一个带来源的事实。subject/object 是实体，predicate 是关系，source 是支撑事实的原始文档 ID。

本题从人工提供的事实开始，隔离图建模本身。不要把手工事实输入称为已经实现了 LLM 实体抽取或实体消歧。

## 任务

完成 `build_knowledge_graph(triples)`，返回 `dict[str, list[Triple]]`：

- 对四个字符串字段去掉两端空白；任何字段为空白时抛 `ValueError`，不修改输入 Triple。
- 保留大小写，`Alice` 与 `alice` 是不同实体；别名消歧属于后续扩展。
- 所有 subject 和 object 都要成为图中的键；每个键的列表仅存该实体的出边，不自动添加反向关系。
- 规范化后四个字段完全相同的事实去重。同一事实来自不同 source 时保留多份证据。
- 图键按实体字符串升序插入；出边按 `(subject, predicate, object, source)` 字符串元组升序排列，保证输出可复现。
- 空输入返回 `{}`，自环合法。

## 验收

```bash
python -m pytest --run-exercises tests/rag/graph/test_level01_knowledge_graph.py -q
```

完成标准：测试通过；加载 [facts.json](../data/facts.json) 后，能指出每条边对应哪份文档，并解释为什么不能凭空补上反向边。

[graph_data/](../data) 与基础文档目录分离，使用独立的事实与原文样本。事实和原文都是教学数据，不涉及自动抽取的置信度。

下一步：[Level 2：多跳图检索与证据回溯](02_graph_retrieval.md)。
