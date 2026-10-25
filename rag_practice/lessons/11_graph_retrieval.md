# Level 11：GraphRAG · 多跳图检索与证据回溯

**本级只解决：答案需要连接多个事实时，怎样找到关系路径和对应原文？**

前置：Level 10，建议已完成 Level 4、Level 6。本级由调用者提供起止实体，先不处理自然语言实体链接。

## A：有界的关系路径

完成 [level11_graph_retrieval.py](../level11_graph_retrieval.py) 的 `find_paths(graph, start, target, max_hops=3)`。

- graph 满足 Level 10 的结构契约，规模不超过 30 个实体。
- start/target 去掉两端空白；空白时抛 `ValueError`。max_hops 是 1–4 的整数，超出范围抛 `ValueError`。
- 返回所有长度为 1 至 max_hops 的有向简单路径，每条路径是按行走顺序排列的 Triple 列表；路径中实体不得重复。
- 不添加反向边。未知实体、无路径或 start==target 时返回 `[]`，本题不返回零长度路径。
- 来源不同的边代表不同证据路径，即使 subject/predicate/object 相同也保留。
- 路径按其边的 `(subject, predicate, object, source)` 元组序列进行字典序排序，不修改输入图。

例如 Alice → Atlas → VectorStore 需要两跳；max_hops=1 时不能返回这条路径。具体关系标签仍由原始 Triple 保留。

## B：图与原文一起支持回答

完成 `answer_graph_question(question, start, target, graph, documents, generator, max_hops=3)`：

- question 去掉两端空白，空白时抛 `ValueError`，不检索或生成；其余参数校验沿用 A。
- 复用 `find_paths`。没有路径时返回 `{"answer": "I don't know based on the provided documents.", "sources": [], "paths": []}`，不调用 generator。
- 按已排序路径的先后遍历各条边，完全相同的 Triple 仅保留第一次，得到 facts；再按事实的首次来源顺序去重得到 sources。
- documents 是 `source -> Document` 映射，约定文档 metadata 中的 source 与键一致；必须为每个 source 找回原文。有缺失时抛 `KeyError`，不生成答案。
- 调用 `generator(normalized_question, facts, ordered_documents)` 一次，返回 `{"answer": 生成文本, "sources": 来源列表, "paths": 检索路径}`。依赖异常直接传播，不修改输入。

生成器同时收到结构化关系和原始证据，而不只是实体名字。图中存在一条路径并不保证关系可以传递：不能把 `WORKS_ON` 接 `USES` 自动改写成未经证据支持的新关系。

## 验收与范围

```bash
python -m pytest --run-exercises tests/rag/test_level11_graph_retrieval.py -q
```

完成标准：测试通过，用样例图展示一跳、两跳、无路径、存在环和缺少来源文档的情况，并解释边方向和证据来源。

这是 **GraphRAG 局部图检索的教学版本**，不是微软完整 GraphRAG 管线。微软的 local search 结合图结构与原始文本；完整方案还包含实体抽取、社区层级、社区摘要和 global search 等部分。[Local Search](https://microsoft.github.io/graphrag/query/local_search/)、[GraphRAG 概览](https://microsoft.github.io/graphrag/)

后续可选项目：实体抽取与别名合并 → 图证据与向量候选融合 → 社区发现与摘要 → 全局问题检索。它们目前是扩展方向，没有伪装成已提供的实现或验收题。
