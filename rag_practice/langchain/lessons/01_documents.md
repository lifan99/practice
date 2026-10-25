# Level 1：文档与来源

**本级只解决：怎样把本地文件变成可追溯的 Document？**

前置：Python 文件读写、Path、列表与字典。学习 `Document.page_content` 和 `Document.metadata` 即可；无需 embedding、向量数据库或 LLM。

## 任务

完成 [level01_documents.py](../exercises/level01_documents.py) 中的 `load_documents(directory: Path) -> list[Document]`。

- 只读取指定目录本层扩展名严格为 `.md` 的文件，不递归。
- 按文件名升序返回；UTF-8 读取，去掉内容两端空白，忽略空白文件。
- 每份文档的 `metadata["source"]` 为文件名，不是绝对路径。
- 目录不存在时抛 `FileNotFoundError`；路径不是目录时抛 `NotADirectoryError`。
- 存在但没有有效文件时返回 `[]`。

例如，目录含 `b.md`（内容为 ` graph `）和 `a.md`（内容为 `prompt`），返回文档内容顺序应为 `prompt`、`graph`，source 顺序为 `a.md`、`b.md`。

## 验收

在仓库根目录运行：

```bash
python -m pytest --run-exercises tests/rag/langchain/test_level01_documents.py -q
```

完成标准：测试通过，并能解释内容与 metadata 各自的用途。不要把 source 信息拼进原始正文来代替 metadata。

下一步：[Level 2：文档切分](02_chunking.md)。
