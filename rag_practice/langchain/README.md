# RAG：LangChain 集成

本路径练习框架边界和组件替换。先用核心手写路径理解机制，再学习 Document、递归 splitter、InMemoryVectorStore、Runnable 和模型消息。每级任务有独立测试，不要求接真实 API。

| 级别 | 能力 | 任务 | 代码 |
| --- | --- | --- | --- |
| 1 | 文件与 Document | [说明](lessons/01_documents.md) | [代码](exercises/level01_documents.py) |
| 2 | 固定窗口与递归 splitter | [说明](lessons/02_chunking.md) | [代码](exercises/level02_chunking.py) |
| 3 | InMemoryVectorStore 与检索 | [说明](lessons/03_retrieval.md) | [代码](exercises/level03_retrieval.py) |
| 4 | 证据格式与消息 | [说明](lessons/04_generation.md) | [代码](exercises/level04_generation.py) |
| 5 | 问答组合与空证据分支 | [说明](lessons/05_pipeline.md) | [代码](exercises/level05_pipeline.py) |
| 6 | source 级召回评估 | [说明](lessons/06_evaluation.md) | [代码](exercises/level06_evaluation.py) |
| 7 | 两路 Runnable 与 RRF | [说明](lessons/07_hybrid.md) | [代码](exercises/level07_hybrid.py) |
| 8 | 重排与正文字符预算 | [说明](lessons/08_reranking.md) | [代码](exercises/level08_reranking.py) |
| 9 | 核心 Chunk 与框架模型／检索器桥接 | [说明](lessons/09_bridge.md) | [代码](exercises/level09_bridge.py) |

## 运行

安装根目录 requirements-lock.txt，在仓库根目录执行：

```bash
python -m pytest --run-exercises tests/rag/langchain/test_level01_documents.py -q
python -m pytest --run-exercises tests/rag/langchain/test_level09_bridge.py -q
python -m pytest --run-exercises tests/rag/langchain -q
```

核心 [core/](../core/README.md) 使用自定义数据结构，桥接题把模型和检索器转成普通回调；同一个核心问答流程可以复用。框架基础题保留 Document/Runnable 类型，以练习框架的原生接口。

## 对照与实验

文档题清理首尾空白，核心文档题保留原文偏移；评估题按 source 算召回，核心评估按 chunk 计算；本路径第8级使用正文字符预算，核心第9级用完整渲染证据的 token 预算。比较实现前明确口径，不强行把不同语义的类型或分数互换。

桥接后的中性score仅用于接口兼容，不代表真实相似度。固定模型和关键词向量只检查传递与执行；真实质量需按[综合实验](../core/experiments/README.md)单独记录。返回 [RAG 总路径](../README.md)。
