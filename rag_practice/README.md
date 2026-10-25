# RAG 分级练习：先手写，再接框架

主路径调整为 **手写基础 → 手写进阶检索 → 框架适配 → LangGraph／GraphRAG 扩展**。RAG 是架构，学习核心机制无需先掌握 LangChain。任务提供中文契约、代码骨架和独立测试，核心实现留给学习者。

## 第一阶段：框架无关的手写主线

进入 [core/README.md](core/README.md)。十级使用自定义 Document／Chunk／SearchHit 和普通 Python 回调；核心代码只依赖标准库，可选 NumPy。不允许用现成检索器代替指定算法。

| 级别 | 内容 | 任务 |
| --- | --- | --- |
| C1 | 原文读取、来源 | [说明](core/lessons/01_documents.md) |
| C2 | 重叠窗口、段落聚合、原文偏移 | [说明](core/lessons/02_chunking.md) |
| C3 | 余弦相似度、精确 Top-k | [说明](core/lessons/03_vectors.md) |
| C4 | 自有索引、向量快照、检索前过滤 | [说明](core/lessons/04_index.md) |
| C5 | 手写 BM25 | [说明](core/lessons/05_bm25.md) |
| C6 | 普通函数问答、证据格式、空结果拒答 | [说明](core/lessons/06_pipeline.md) |
| C7 | 手写 Recall、MRR、NDCG、固定集评估 | [说明](core/lessons/07_metrics.md) |
| C8 | RRF、关键词与向量混合检索 | [说明](core/lessons/08_hybrid.md) |
| C9 | 注入重排模型、完整证据 token 预算 | [说明](core/lessons/09_context.md) |
| C10 | 多查询扩展、去重、调用上限、排名融合 | [说明](core/lessons/10_multiquery.md) |

C1–C7建立机制和评估基线；C8–C10再增加检索策略。embedding、生成、分词和重排模型通过接口注入，不要求训练模型。完成后做[综合对比实验](core/experiments/README.md)，说明复杂度、失败样本和实际观测结果。

```bash
# Minimal dependencies for the core track only.
python -m pip install -r requirements-rag-core.txt
python -m pytest --run-exercises tests/rag/core/test_core01_documents.py -q
python -m pytest --run-exercises tests/rag/core -q
```

只安装最小依赖时不要运行其他主题测试；原有完整环境也可直接运行。依赖安装后核心测试离线，无需 API Key。

## 第二阶段：LangChain 适配与框架对照

进入 [adapters/README.md](adapters/README.md)，完成 Chunk 与 LangChain Document 的双向转换、Runnable retriever 和 chat model 的普通回调适配。复用手写主线的同一问答接口，检查 ID、来源、偏移和消息传递，再替换模型或向量存储。

```bash
python -m pip install -r requirements-lock.txt
python -m pytest --run-exercises tests/rag/adapters -q
```

原有文件和测试入口继续保留，已经开始的实现无需迁移。下面旧 L1–L8 现在作为后续框架对照，原编号不等同于新 C1–C10：

| 原编号 | 定位 | 任务／代码 |
| --- | --- | --- |
| L1 | LangChain Document 文件读取 | [说明](lessons/01_documents.md)／[代码](level01_documents.py) |
| L2 | 窗口对照与递归 splitter | [说明](lessons/02_chunking.md)／[代码](level02_chunking.py) |
| L3 | InMemoryVectorStore | [说明](lessons/03_retrieval.md)／[代码](level03_retrieval.py) |
| L4 | messages／模型输入 | [说明](lessons/04_generation.md)／[代码](level04_generation.py) |
| L5 | Runnable 问答组合 | [说明](lessons/05_pipeline.md)／[代码](level05_pipeline.py) |
| L6 | source 级召回评估 | [说明](lessons/06_evaluation.md)／[代码](level06_evaluation.py) |
| L7 | 双路 Runnable 与 RRF | [说明](lessons/07_hybrid.md)／[代码](level07_hybrid.py) |
| L8 | 重排回调与字符预算 | [说明](lessons/08_reranking.md)／[代码](level08_reranking.py) |

旧测试示例：`python -m pytest --run-exercises tests/rag/test_level03_retrieval.py -q`。ex01_index.py、ex02_qa.py仍指向旧练习；原有前置笔记也服务于旧 Document 题。新主线保留原文偏移，旧读取题清理首尾空白，两者契约不要混用。新 C7 是 chunk 级指标，旧 L6 是 source 级指标；新 C9 计完整证据的 token，旧 L8 计正文字符。

## 第三阶段：工作流与知识图谱

| 分支 | 任务 | 前置 |
| --- | --- | --- |
| LangGraph RAG | [L9：证据评估、改写、有界纠正检索](lessons/09_workflow.md) | 手写流程与评估、LangGraph 基础；此分支使用 Document／Runnable |
| GraphRAG | [L10：事实图建模](lessons/10_knowledge_graph.md) | 有向图、来源追踪；本级自身使用 dataclass |
| GraphRAG | [L11：局部多跳检索与原文证据](lessons/11_graph_retrieval.md) | L10；原文适配仍使用 LangChain Document |

工作流图的节点是执行步骤，知识图谱的节点是实体。静态回调不等于自主规划；GraphRAG 这里只覆盖局部图检索，不包含自动实体抽取、社区摘要和全局检索。

## 验收边界

默认 pytest 跳过学生练习，只检查环境；--run-exercises 才执行验收。TODO 初始失败是预期现象；公开测试通过后仍需解释机制、增加反例并完成实验。

[data/](data/) 的三份 Markdown 与旧 [evaluation_queries.json](data/evaluation_queries.json) 适合组件连通性实验；[graph_data/](graph_data/) 服务图检索分支。关键词向量和固定模型回复不证明真实语义质量。手写主线需建立自己的 chunk 级证据标签，不直接把旧 source 标签当作 chunk_id。

真实模型、语义重排、持久化数据库、增量更新、部署、权限、HNSW／IVF 均可作为后续项目。增加组件不保证质量提升；用固定问题集报告质量、证据支持、延迟、调用次数与成本。
