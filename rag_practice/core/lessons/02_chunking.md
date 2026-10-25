# C2：窗口与段落，保留原文位置

目标：亲手实现 [window_chunks / paragraph_chunks](../exercises/level02_chunking.py)，不得调用现成 splitter。每块来源与输入相同，ID 严格为 `source:start:end`；text 是原文对应切片，不额外 strip。

## A：重叠窗口

size>0、0<=overlap<size，否则 ValueError，空文档也先校验。起点从 0 开始，相邻起点相距 size-overlap；终点不越界。当前窗口已到文档末尾就结束，不额外产出被前一块完全包含的尾块。空文本返回 []，空白文本仍参与窗口切分。

`abcdefghij`、size=4、overlap=1 的位置为 (0,4)、(3,7)、(6,10)。说明相邻重叠关系以及为什么循环一定终止。

## B：段落聚合

max_chars>0，否则 ValueError。本题段落分隔符固定为正则 `\n[ \t]*\n` 的匹配，重复空行造成的空白段落忽略；不要求通用 Markdown 解析。

- 每段去除首尾空白得到有效原文区间；全空白段落忽略。
- 从前往后尽量将连续有效段落放入同一块，预算计算为首段起点到末段终点的**整个原文区间**，包括中间原始空白和换行。加下一段超出预算，就结束当前块。
- 一个有效段落本身超过预算时，单独按 max_chars 的无重叠窗口拆开；这些块不再与前后段落合并。
- 空／全空白文档返回 []；不丢弃有效段落中的正文字符。禁止为了符合长度而删除中间字符。

例如 `a\n\n1234567\n\nb`、预算3，正文块为 a、123、456、7、b。所有块都应满足原文切片不变量。

```bash
python -m pytest --run-exercises tests/rag/core/test_level02_chunking.py -q
```

完成后比较：窗口截断、段落切分对句子和证据的影响；字符长度与 token 长度的区别。说明复杂度时把输出文本的复制量计入。
