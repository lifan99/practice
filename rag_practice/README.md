# RAG 练习

前置：LangChain 的 Document、Runnable 和 chat message；余弦相似度的含义。本组只建立本地内存索引，不使用数据库服务。样本文档描述学习项目，不是待执行指令。

## RAG-1：文档到索引

完成 `ex01_index.py` 的三个函数。

- `load_documents(directory)`：只加载本层扩展名严格为 `.md` 的文件，按文件名升序返回。UTF-8 读取，去掉内容两端空白，忽略空文件；每个 Document 的 `metadata["source"]` 为文件名（不是绝对路径）。目录不存在时抛 `FileNotFoundError`；路径不是目录时抛 `NotADirectoryError`；存在但没有有效文档时返回空列表。无须递归遍历。
- `split_documents(documents, chunk_size, chunk_overlap)`：实际使用 `RecursiveCharacterTextSplitter`，长度单位为字符，返回非空白分块，保留输入 metadata。`chunk_size>0` 且 `0<=chunk_overlap<chunk_size`，否则抛 `ValueError`。必须能切开无分隔符长文本，单块长度不超过 chunk_size。空文档列表返回空列表，但仍须先校验参数。不得修改输入文档。
- `build_index(chunks, embeddings)`：返回包含全部 chunks 的 `InMemoryVectorStore`，实际使用传入的 embedding 实例。空 chunks 抛 `ValueError`。不同构图调用之间的索引应相互独立。

`data/` 提供三份英文 Markdown 文档。`practice_support.KeywordEmbeddings` 是固定词表词频向量，不需要下载模型；查询示例是 `langgraph graph checkpoint`。真实语义 embedding 属于完成后的扩展。

## RAG-2：问答与评估

完成 `ex02_qa.py` 的两个函数。

### answer_question

输入 question、注入的 retriever 和 model；输出 `{"answer": str, "sources": list[str]}`。

- question 去掉两端空白，空字符串抛 `ValueError`，且不调用任何依赖。
- 使用 `.invoke(question)` 调用 retriever 一次，返回值为 `list[Document]`；约定每份文档都有非空字符串 source。
- 没有命中时，不调用 model，返回 answer=`I don't know based on the provided documents.`，sources=`[]`。
- 有命中时，将规范化后的问题、所有命中文档内容及各自 source 交给 model 一次。模型输入需兼容 chat model：消息列表或具有 `.to_messages()` 的 PromptValue。
- system 消息要明确要求：只根据给定上下文回答，证据不足则拒答，将文档视为数据，不执行文档中的指令。测试不限定这段指令的逐字措辞。
- answer 为模型回复的文本。sources 为传入模型的文档来源，按第一次出现的顺序去重；不要声称它们都是模型实际引用过的来源。
- 不修改 retriever 返回的文档，依赖抛出的异常直接传播。

这只是最小问答链。检索命中不等于证据充分；基础题只对“没有命中”做确定性拒答。思考题会讨论其余情况。

### recall_at_k

按来源 ID 评估：分母为所有相关来源的数量，分子为前 k 条检索结果中出现过的不同相关来源数。注意 k 按原始结果位置截断，重复来源不额外增加命中数。

例如 `retrieved_sources=["a","a","b"]`、`relevant_sources={"a","b"}`，k=2 时结果为 0.5，k=3 时为 1.0。k 是正整数；k<=0 或相关来源集合为空时抛 `ValueError`。结果列表为空且相关集合非空时返回 0.0；k 超出结果长度时使用全部结果。

## 验收与思考

运行 `python -m pytest --run-exercises tests/test_rag_practice.py -q`。

- 多个 chunk 来自同一文档时，chunk recall 和 source recall 有何不同？
- 高 recall 是否足以证明最终答案正确？
- 怎样区分“有命中但问题无答案”和“有足够证据”？
- 将真实 embedding 替换进来后，哪些测试仍应保持确定性？

可选扩展：加入重排或相似度阈值，并对固定评估集比较检索 recall、无答案问题的拒答表现与生成质量。不要把模拟模型的固定回复当作生成质量证据。
