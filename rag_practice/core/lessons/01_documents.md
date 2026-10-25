# C1：原文与来源

目标：不依赖框架读取可追溯文档。完成 [load_documents](../exercises/level01_documents.py)，返回本包 [Document](../types.py)。

- 只读指定目录本层扩展名严格为 .md 的普通文件，忽略目录和其他后缀；按文件名升序返回。
- UTF-8 解码；只用 strip 判断是否为空白，**返回正文保留原来的前后空白**，为后续原文位置提供稳定坐标。
- source 为文件名；正文与来源分开保存。无有效文件返回 []。
- 不存在抛 FileNotFoundError；路径为文件抛 NotADirectoryError；解码或读取失败直接传播。

例：a.md 内容为 `  中文\n`，返回 Document.text 仍为该原始字符串。

```bash
python -m pytest --run-exercises tests/rag/core/test_level01_documents.py -q
```

完成后解释：strip 后的偏移为什么不能直接用于定位原文件？框架文档题使用清理后的正文；手写核心为位置溯源保留原文，跨接口对照前应统一正文口径。
