# Level 4：真实 stdio client 与生命周期

**本级只解决：怎样启动、使用并关闭一个本地 MCP server 子进程？**

完成 [level04_stdio.py](../level04_stdio.py) 的异步函数 inspect_stdio(server)。server 是 StdioServerParameters，测试指向提供的 [reference_server.py](../reference_server.py)，不依赖 Level 2 的实现。

- 使用 SDK v2 的 Client 与异步上下文；不手写进程管理或 JSON-RPC。
- 发现工具，按 name 排序；调用 echo，arguments=`{"message":"hello"}`；读取 `health://ready`。
- 返回 `{"tools":["echo"],"echo":"hello","health":"ready"}`，echo 从 structured_content 的 result 字段读取，health 从资源的文本内容读取。
- 离开函数时关闭连接与子进程，即使调用失败也要释放；依赖异常原样传播。
- 不额外创建 MCP server，不向 stdio 子进程的 stdout 打印其他信息。

```bash
python -m pytest --run-exercises tests/mcp/test_level04_stdio.py -q
```

测试使用当前虚拟环境的 sys.executable、模块入口和明确 cwd，不依赖当前终端的 PATH。新协议的发现与兼容性由 Client 管理；这里不照搬旧 SDK 的 ClientSession.initialize 流程。

下一步：[Level 5](05_http.md)。
