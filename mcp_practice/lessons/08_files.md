# Level 8：文件资源的应用边界

**本级只解决：资源 handler 如何限定可读取的本地文件？**

完成 [level08_files.py](../level08_files.py) 的两个辅助函数，之后可接入自己的 resource handler。

- resolve_note_path(root, relative_path) 仅返回 root 内已存在的 Markdown 文件的解析后绝对 Path，不读取正文。
- root 不存在抛 FileNotFoundError，不是目录抛 NotADirectoryError。
- relative_path 使用 `/` 分隔；空白、绝对路径、含反斜线、冒号、NUL 或 `..` 路径段时抛 ValueError。允许 `.` 路径段。
- 请求路径和解析后的目标扩展名都必须严格为 `.md`，否则 ValueError；缺失文件抛 FileNotFoundError，目录抛 IsADirectoryError。
- 解析符号链接后仍须位于解析后的 root 内，外部目标抛 PermissionError；内部符号链接可以读取。
- read_note 复用 resolver，以 UTF-8 原样读取，不 strip，不返回绝对路径给模型充当正文。

```bash
python -m pytest --run-exercises tests/mcp/test_level08_files.py -q
```

这是应用级路径解析练习，不实现操作系统沙箱、OAuth 或文件被并发替换时的无竞态读取。新协议里 roots 已被弃用，不把旧 roots 机制当作本题的访问授权。

下一步：[Level 9](09_langchain.md)。
