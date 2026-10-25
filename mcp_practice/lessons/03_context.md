# Level 3：Resources、URI 模板与 Prompts

**本级只解决：读取上下文和取得提示模板，怎样与执行工具区分？**

完成 [level03_context.py](../level03_context.py) 的 build_notes_server(notes)。notes 是笔记名到正文的映射，名字约定仅含英文字母、数字、下划线，正文为字符串。

- 返回独立 MCPServer，使用构建时的 notes 快照，不修改传入映射。
- 注册静态资源 `notes://catalog`，内容为按笔记名排序后以换行连接的名字，空映射时为空串。
- 注册资源模板 `note://{name}`，读取指定笔记的原始正文，mime_type=`text/plain`。
- 注册 prompt `study_note`，参数为 name，返回一条 user 文本消息，内容严格为 `Explain this note:\n` 加笔记正文。可以返回字符串，由 SDK 包装消息。
- 未知笔记通过 SDK 报告调用错误，不伪装成空白资源或成功提示词。

```bash
python -m pytest --run-exercises tests/mcp/test_level03_context.py -q
```

完成标准：分别发现静态资源、URI 模板和 prompt，读到实际正文与消息；解释 prompt 是供客户端使用的模板，不是在 MCP server 内自动运行的模型调用。

下一步：[Level 4](04_stdio.md)。
