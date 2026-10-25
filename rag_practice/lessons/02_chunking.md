# Level 2：从字符窗口到递归切分

**本级只解决：怎样把长文档拆成保留来源的小块？**

前置：Level 1、字符串切片。先完成 A，再完成 B。本级不建立索引，不调用模型。

## A：固定字符窗口

完成 [level02_chunking.py](../level02_chunking.py) 的 `fixed_size_chunks(text, chunk_size, chunk_overlap=0)`，返回 `list[str]`。

- 长度单位为 Python `len()` 计量的字符数，不是 token。
- 按原文顺序返回字符窗口，单块最多 chunk_size 个字符，相邻窗口重叠 chunk_overlap 个字符。
- 原文末尾已包含在当前块中时结束，不再产生一个仅重复末尾内容的窗口。
- 保留空白，不调用 `.strip()`；不得丢失任何原文字符。空字符串返回 `[]`。
- 必须满足 `chunk_size>0` 且 `0<=chunk_overlap<chunk_size`，否则抛 `ValueError`；空输入也先校验参数。只要求处理整数参数。
- 本小题使用 Python 字符串操作，不调用 splitter 库。

公开例子：`fixed_size_chunks("abcdefghij", 4, 1)` 返回 `["abcd", "defg", "ghij"]`；`fixed_size_chunks("abcd", 4, 1)` 只返回 `["abcd"]`。

## B：递归切分与 metadata

完成同一文件的 `split_documents(documents, chunk_size=160, chunk_overlap=30)`，实际使用 `RecursiveCharacterTextSplitter`。

- 参数校验与 A 相同；空文档列表返回 `[]`。
- 返回非空白 Document 分块，每块长度不超过 chunk_size；无分隔符的长文本也能被切开。
- 保留每份输入文档的 metadata，不修改输入对象。不同输入文档的内容不得混成一个块。
- 对普通段落优先保留自然边界，可配置中文标点；本小题不限定分隔符的具体列表。
- 库的 chunk_overlap 是目标重叠量，不要求每两个输出块恰好重叠该数量。

两小题有意保留不同契约：A 原样保留字符，B 可以按库规则清理块边缘空白，但不能丢掉非空白正文。

## 验收与观察

```bash
python -m pytest --run-exercises tests/rag/test_level02_chunking.py -q
python -m pytest --run-exercises tests/rag/test_level02_chunking.py -k fixed -q
```

完成标准：两部分测试通过，能解释大小和重叠的单位。再用同一段中文分别观察 size=40/80、overlap=0/10 的结果，记录块数、句子边界和重复内容；此观察不设唯一正确参数。

下一步：[Level 3：向量检索](03_retrieval.md)。
