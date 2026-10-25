# 第二阶段：LangChain 适配与组件替换

先完成 [RAG 手写主线](../core/README.md)与固定集评估，再把框架接在边界上。此阶段需要根目录 requirements-lock.txt；核心代码仍只使用自己的 dataclass 和普通回调。

## A：桥接练习

完成 [langchain_bridge.py](langchain_bridge.py)，不附实现。

- to_langchain：Chunk.text→page_content；metadata 严格为 chunk_id、source、start、end 四个字段，值原样复制，不共享可变字典。
- from_langchain：四个字段必须齐全；ID/source 为非空单行字符串；start/end 为整数且非 bool，0<=start<=end，end-start==len(page_content)，否则 ValueError。允许额外 metadata，但不放进核心 Chunk。不读取磁盘，不声称仅凭偏移即可验证正文与原文一致。
- as_core_retriever：返回普通函数，构造适配器时不调用依赖。执行时将传入 query 原样交给 Runnable.invoke 一次；结果约定 list[LangChain Document]，逐项经 from_langchain 转为 SearchHit，score 固定0（中性占位，不伪造框架未返回的相关分），顺序不变。
- as_core_chat_model：返回普通函数；把核心 system/user 消息转换成对应 SystemMessage/HumanMessage，按输入顺序调用 model.invoke 一次，返回 AIMessage.content。输入只含这两种 role；约定模型 content 是字符串。本题不处理多模态块、tool messages 或流式输出。
- 输入不修改；依赖异常传播。本阶段可用 RunnableLambda / FakeListChatModel 验证边界，无需真实API。

```bash
python -m pytest --run-exercises tests/rag/adapters -q
```

然后让同一个 C6 answer_question 先接本地普通回调，再接上述适配器，核对消息、chunk_id 与来源一致。中性score只用于接口兼容，不能作为相似度阈值依据。

## B：原有框架练习的定位

旧 levelXX 文件及测试路径继续可用，其中的 Document/Runnable/InMemoryVectorStore 题现在属于**后续框架对照**，不再作为学习 RAG 的前置条件。已经写的代码可继续完成，无需迁移。新旧文档切分契约不同，先明确正文是否清理，再比较偏移，不能强行互换。

| 手写能力 | 后续框架对照入口 | 目的 |
| --- | --- | --- |
| C1–C2 | [旧文档题](../lessons/01_documents.md)、[旧切分题](../lessons/02_chunking.md) | 对照 Document 与递归 splitter |
| C3–C4 | [旧检索题](../lessons/03_retrieval.md) | 用 InMemoryVectorStore 替换自有索引 |
| C6 | [旧生成题](../lessons/04_generation.md)、[旧组合题](../lessons/05_pipeline.md) | 对照 messages/Runnable |
| C7–C9 | [旧评估题](../lessons/06_evaluation.md)、[融合](../lessons/07_hybrid.md)、[重排](../lessons/08_reranking.md) | 比较 source指标与chunk指标、字符预算与token预算 |

旧测试：`python -m pytest --run-exercises tests/rag/test_level03_retrieval.py -q`。更多选择见[总路径](../README.md)。

真实模型、向量数据库集成另行安装 provider 包并配置凭据；不要求重写模型训练。替换时保持数据、embedding 与评估口径稳定，记录真实延迟、质量和成本。
