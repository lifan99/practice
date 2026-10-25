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

## 已完成手写核心时怎么选

本路径是框架集成分支，不是完成核心后必须再做一轮的机制主线。先阅读 L1–L3，识别 Document、splitter 与向量存储的类型和语义；结合 LangChain 基础消息接口完成 L9 桥接，再用同一个核心问答流程验证替换。

L1–L8 中已能独立实现的机制可跳过重复代码题，前提是提交一份框架替换迁移证据：原文／ID／偏移／来源往返无损、同一问题与固定 chunks 的结果可对照、失败行为可解释，并明确下述评估与预算口径差异。使用了特定框架组件时仍需验证其原生行为；不会的部分回到对应级别练习。桥接测试不能代替向量存储本身的验证。

没有完成的题仍保持 TODO，不把跳过称为测试通过；运行验收时只选已完成单元。项目是否采用框架由需求决定，进入 [P2](../../projects/knowledge-assistant/02_service.md)无需先完成本路径九级。

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
