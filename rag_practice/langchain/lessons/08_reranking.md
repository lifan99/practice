# Level 8：Advanced RAG · 重排与上下文预算

**本级只解决：候选已经找回后，怎样把有限的上下文交给模型？**

前置：Level 3、Level 6；可以接在 Level 7 后。先区分两件事：召回负责候选覆盖，reranking 负责在这些候选中重新排序。本级不重新实现 embedding 或 cross-encoder。

## A：注入重排评分器

完成 [level08_reranking.py](../exercises/level08_reranking.py) 的 `rerank(question, documents, scorer, top_k=3)`。

- question 去掉两端空白；空白问题或 top_k<=0 抛 `ValueError`，不调用 scorer。top_k 是整数。
- 先按 `metadata["chunk_id"]` 去重，保留首次出现的文档。每个不同 chunk 恰好调用一次 `scorer(question, page_content)`。
- 分数越大越相关；分数相同保持原候选顺序。返回最多 top_k 个 Document，不修改文档或 metadata。
- 约定 chunk ID 非空，相同 ID 内容一致；分数是实数，负数合法，NaN 或正负无穷抛 `ValueError`。空候选返回 `[]`；依赖异常直接传播。

测试评分器是本地函数，验证调用和排序。真实 semantic reranker 可以通过同一个接口接入；测试通过不代表已经实现或验证了 cross-encoder 模型。

## B：完整块的预算选择

完成 `pack_context(documents, max_chars)`，按当前顺序考虑每块：仅在整块正文能放入剩余预算时选入，否则跳过该块，继续考虑后面的块。

- 返回选中的 Document，保留相对顺序；不截断正文、不修改输入。输入约定已去重且正文非空。
- 预算只按 `len(page_content)` 计量，正好用满允许；max_chars 是正整数，否则抛 `ValueError`。
- 空输入返回 `[]`。这不是最优组合求解题，也不要求重排输出。
- 本题字符预算不包含标题、分隔符、问题或 system message，不能据此保证真实模型 token 限额；完整提示词的 tokenizer 预算属于扩展。

例如块长度依次为 8、20、2，预算 10 时选择第一块和第三块。

## 验收与比较

```bash
python -m pytest --run-exercises tests/rag/langchain/test_level08_reranking.py -q
```

完成标准：测试通过，并分别记录重排前、重排后、预算选择后的候选及支持答案的证据是否仍在。不要把“字符更少”自动解释成“答案更好”。

[Semantic reranking 官方说明](https://www.elastic.co/docs/solutions/search/ranking/semantic-reranking)。下一步可选：[Level 9 的 LangGraph 工作流](../../workflows/lessons/01_corrective.md) 或 [Level 10 的知识图谱分支](../../graph/lessons/01_knowledge_graph.md)。
