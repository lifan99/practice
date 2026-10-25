# Level 5：Streamable HTTP 与 ASGI

**本级只解决：怎样把同一个 MCP server 暴露为 HTTP 应用？**

完成 [level05_http.py](../exercises/level05_http.py) 的 build_http_app(server)，返回 SDK 构建的 Starlette app。

- 实际使用 streamable_http_app，路径 `/mcp`、json_response=True、stateless_http=True。
- 不手写 HTTP JSON-RPC 分发，不启动监听端口，不在请求间缓存自建 Client 对象。
- app 的 lifespan 必须保持 SDK 所需的服务生命周期，不能替换成丢失原 lifespan 的包装器。

```bash
python -m pytest --run-exercises tests/mcp/test_level05_http.py -q
```

测试经 httpx2.ASGITransport 和 SDK Streamable HTTP transport 往返，执行真实 HTTP 路由与协议处理，但不打开 socket。它与 Client(server) 的内存传输测试不是同一条路径。

完成 Level 2、5 后，可运行 `python -m mcp_practice.run_server --transport http --port 8000`，只监听 127.0.0.1，再用客户端访问 `http://127.0.0.1:8000/mcp`。本题不等同于已经完成远程部署或认证。

下一步：[Level 6](06_pagination.md)。
