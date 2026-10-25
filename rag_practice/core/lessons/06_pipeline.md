# C6：用普通函数串起 RAG

目标：实现 [format_context / answer_question](../level06_pipeline.py)，不使用 Runnable、PromptTemplate、Document 或 chain。回调和数据结构见 [types.py](../types.py)。

## A：证据格式

format_context 接收 chunks，按顺序输出 `[chunk_id|source]\n正文`，块间用两个换行分隔。保留原文，空列表返回空字符串。这里输入 ID、source 为单行字符串。此函数只格式化，不去重。

## B：问答

- question.strip() 为空抛 ValueError，且不调用依赖。
- 清理后问题传给 retrieve 一次，获得 list[SearchHit]。按 chunk_id 去重，保留首次命中；不按来源合并块。输入 hits 的分数不在本级用于阈值判断。
- 空结果返回 `{"answer":"未找到足够的证据。","sources":[],"chunk_ids":[]}`，不调用生成回调。
- 非空时复用本模块 format_context，生成恰好两条普通 dict 消息，role 依次为 system、user。system 表达“仅依据证据、证据不足则说明无法回答、证据正文不作为指令”；措辞自定。user 必须包含原始清理后问题和完整证据。
- generate(messages) 恰好一次，返回的字符串作为 answer。sources 按选中块的首次出现顺序去重；chunk_ids 按选中块顺序返回。
- 不修改输入；异常传播；禁止查询内容到答案的硬编码。

```bash
python -m pytest --run-exercises tests/rag/core/test_core06_pipeline.py -q
```

完成标准：测试通过，并人工检查 system 文本三项要求。模拟生成器只证明输入组织和分支正确，不能证明真实模型会拒答、防注入或正确引用。来源列表表示提供过的证据，不自动代表模型实际使用过这些来源。
