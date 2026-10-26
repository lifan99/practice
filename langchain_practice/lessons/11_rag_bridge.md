# Level 11：RAG 核心接口与 LangChain 桥接

前置：[RAG 核心类型](../../rag_practice/core/types.py)、[C6 问答接口](../../rag_practice/core/lessons/06_pipeline.md)，以及 [Level 1 消息](01_chain.md)与 [Level 3 Runnable](03_composition.md)。可在完成这些前置后独立选做。

目标：复用已有核心实现，只转换框架边界的类型与调用协议。读取、切分、检索、问答与评估仍在 RAG core 中实现一次。

完成 [level11_rag_bridge.py](../exercises/level11_rag_bridge.py)，不附实现。

- to_langchain：Chunk.text→page_content；metadata 严格为 chunk_id、source、start、end 四个字段，值原样复制，不共享可变字典。
- from_langchain：四个字段必须齐全；ID/source 为非空单行字符串；start/end 为整数且非 bool，0<=start<=end，end-start==len(page_content)，否则 ValueError。允许额外 metadata，但不放进核心 Chunk。不读取磁盘，不声称仅凭偏移即可验证正文与原文一致。
- as_core_retriever：返回普通函数，构造适配器时不调用依赖。执行时将传入 query 原样交给 Runnable.invoke 一次；结果约定 list[LangChain Document]，逐项经 from_langchain 转为 SearchHit，score 固定0（中性占位，不伪造框架未返回的相关分），顺序不变。
- as_core_chat_model：返回普通函数；把核心 system/user 消息转换成对应 SystemMessage/HumanMessage，按输入顺序调用 model.invoke 一次，返回 AIMessage.content。输入只含这两种 role；约定模型 content 是字符串。本题不处理多模态块、tool messages 或流式输出。
- 输入不修改；依赖异常传播。本阶段可用 RunnableLambda / FakeListChatModel 验证边界，无需真实API。

```bash
python -m pytest --run-exercises tests/langchain/test_level11_rag_bridge.py -q
```

然后让同一个 C6 answer_question 先接本地普通回调，再接上述适配器，核对消息、chunk_id 与来源一致。中性score只用于接口兼容，不能作为相似度阈值依据。

