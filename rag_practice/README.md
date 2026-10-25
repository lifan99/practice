# RAG 分级练习

学习路径分为 **基础 RAG → Advanced RAG → 工作流编排 / GraphRAG**。基础六级每次增加一个主要能力，进阶按依赖选择分支；所有代码都是待完成的练习，不附完整答案，不要求先部署数据库或真实模型服务。

## 从哪里开始

基础准备：Python 函数、字典、列表、Path 和类型标注。第 1–3 级无需 chat model；第 4 级开始需要 LangChain messages / Runnable，可先完成仓库的 LangChain 练习。整个基础路径不要求先学 LangGraph。下表是基础六级；进阶路径见后面的独立分组。

| 级别 | 本级要回答的问题 | 题目 | 代码 |
| --- | --- | --- | --- |
| 1 · 文档 | 如何保留内容与来源？ | [任务说明](lessons/01_documents.md) | [level01_documents.py](level01_documents.py) |
| 2 · 切分 | 如何从字符窗口过渡到递归切分？ | [任务说明](lessons/02_chunking.md) | [level02_chunking.py](level02_chunking.py) |
| 3 · 检索 | 如何只找证据、不生成答案？ | [任务说明](lessons/03_retrieval.md) | [level03_retrieval.py](level03_retrieval.py) |
| 4 · 生成 | 给定证据后如何组织模型输入？ | [任务说明](lessons/04_generation.md) | [level04_generation.py](level04_generation.py) |
| 5 · 组合 | 如何处理检索、生成与无证据分支？ | [任务说明](lessons/05_pipeline.md) | [level05_pipeline.py](level05_pipeline.py) |
| 6 · 评估 | 如何测量召回并比较切分配置？ | [任务说明](lessons/06_evaluation.md) | [level06_evaluation.py](level06_evaluation.py) |

每级的说明给出前置知识、输入输出契约、边界情况、独立测试命令和完成标准。第 2 级有先后两道小题，第 6 级另有参数对比实验。

## 如何运行

先按照[总说明](../README.md)安装依赖，然后在仓库根目录执行：

```bash
# Start with level 1 only.
python -m pytest --run-exercises tests/rag/test_level01_documents.py -q

# After completing level 1, move to level 2.
python -m pytest --run-exercises tests/rag/test_level02_chunking.py -q

# Run all RAG acceptance checks when ready.
python -m pytest --run-exercises tests/rag -q
```

初始 `NotImplementedError` 是待完成练习的标记。默认 `python -m pytest -q` 跳过全部练习，只验证运行环境，不能证明你已经完成某级。公开测试通过后，还应对照契约检查边界，并完成本级解释或观察任务。

测试尽量隔离不同级别：第 3 级直接使用提供好的 Document，第 4 级直接使用给定证据，第 5 级用替代生成函数检查组合逻辑，第 6 级用固定 retriever 检查指标。这样某一级的失败不会迫使你同时调试整条链。最终串联时仍需完成前面的组件。

## 数据与范围

- [data/](data/) 包含三份短 Markdown 文档；第 1 级只读取 `.md` 文件。
- [evaluation_queries.json](data/evaluation_queries.json) 给出第 6 级组件实验的问题与相关来源，加载后把来源列表转成 set。
- `practice_support.KeywordEmbeddings` 是本地词频向量；`FakeListChatModel` 返回预设文本。两者用于流程验证，不代表真实语义检索或生成质量。
- 通过 context 传递 source 不证明模型实际引用了它，也不证明回答正确。基础题仅对空检索结果实现确定性拒答。

旧的 `ex01_index.py`、`ex02_qa.py` 保留为导入兼容入口。请修改相应的 `levelXX_*.py`，不要在旧文件重复实现。

## Advanced RAG：改进候选与上下文

先完成 Level 6，建立固定评估集后再加组件。新增机制不保证提升质量，应与基础检索在相同数据和预算下比较。

| 级别 | 能力与前置 | 题目 | 代码 |
| --- | --- | --- | --- |
| 7 · 混合检索 | 两路召回、RRF 排名融合；前置 Level 3、6 | [任务说明](lessons/07_hybrid.md) | [level07_hybrid.py](level07_hybrid.py) |
| 8 · 重排与预算 | 注入重排评分器、选择完整上下文块；前置 Level 3、6，可接 Level 7 | [任务说明](lessons/08_reranking.md) | [level08_reranking.py](level08_reranking.py) |

## LangGraph RAG：管理执行流程

| 级别 | 能力与前置 | 题目 | 代码 |
| --- | --- | --- | --- |
| 9 · 可纠正检索 | 评估证据、改写 query、有界重试与拒答；前置 Level 5、6 和 LangGraph 练习 | [任务说明](lessons/09_workflow.md) | [level09_workflow.py](level09_workflow.py) |

本级的图节点是执行步骤，例如 retrieve、grade、rewrite。它不要求知识图谱；本题提供的是可纠正检索工作流，不把固定流程测试等同于自主 agent 能力。

## GraphRAG：利用实体和关系检索

| 级别 | 能力与前置 | 题目 | 代码 |
| --- | --- | --- | --- |
| 10 · 知识图谱 | 有向事实、来源、去重与规范化；前置文档和有向图基础 | [任务说明](lessons/10_knowledge_graph.md) | [level10_knowledge_graph.py](level10_knowledge_graph.py) |
| 11 · 图证据检索 | 有界多跳路径、原文证据回溯、带关系的生成输入；前置 Level 10，建议 Level 4、6 | [任务说明](lessons/11_graph_retrieval.md) | [level11_graph_retrieval.py](level11_graph_retrieval.py) |

这条分支不依赖 Level 9。这里图节点是实体，边是带来源的关系。使用独立的 [graph_data/](graph_data/) 样本，先隔离图建模和局部检索；人工事实不等于完成了自动实体抽取。

本项目目前覆盖 GraphRAG 的局部图检索教学路径。微软完整 GraphRAG 还涉及社区层级、摘要和 global search；这些属于后续项目，不能把本练习当成完整复刻。[官方概览](https://microsoft.github.io/graphrag/)

## 进阶如何验收

每级仍有独立代码、契约和测试，可以只运行当前级：

```bash
python -m pytest --run-exercises tests/rag/test_level07_hybrid.py -q
python -m pytest --run-exercises tests/rag/test_level09_workflow.py -q
python -m pytest --run-exercises tests/rag/test_level10_knowledge_graph.py -q
python -m pytest --run-exercises tests/rag/test_level11_graph_retrieval.py -q
```

离线测试使用固定 retriever、评分器、grader、rewriter 和 generator，验证排序、数据流、来源与终止条件。它们不证明真实模型具备语义重排、可靠的证据判断、实体抽取或事实推理能力。

基础与进阶都不增加 API Key 要求，也没有引入 Neo4j、Elasticsearch 或额外模型下载。真实服务是替换依赖后的独立实验。

## 后续项目方向

尚未提供实现与验收的方向：多查询改写与融合、父子块检索、结构化文档与表格处理、实体抽取与别名合并、图与向量候选融合、社区摘要与全局检索、持久化与增量更新。每次选一个明确问题，记录改动前后的检索质量、证据完整性、调用次数与成本，不把组件数量当成能力等级。
