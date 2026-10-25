# Level 10：多服务生命周期与工具命名空间

**本级只解决：多个 server 同时接入时，怎样避免资源泄漏和同名混淆？**

完成 [level10_multiserver.py](../level10_multiserver.py)。

## A：作用域内连接

connect_servers(servers) 返回异步上下文管理器，供 `async with` 使用。

- servers 的键是本应用定义的别名：匹配 `[A-Za-z][A-Za-z0-9_]*`，并且不能包含 `__`。这不是 MCP 的通用命名限制。
- 在创建任何 Client 前校验所有别名；按字典顺序构建并进入 `Client(对应配置)`。
- 产生别名到已进入 Client 的映射，不复制或创建替代连接。
- 正常退出、调用者抛错、后续连接进入失败时，已成功进入的客户端按相反顺序释放。未进入成功的连接不当作已进入资源退出。
- 空映射合法，产生 `{}`；不保存全局连接，不吞掉异常。

## B：稳定的工具路由表

namespace_tools(registries) 返回按 public_name 升序排列的 ToolBinding 列表。

- 校验相同别名规则；每个服务内部重复工具名抛 ValueError，不同服务可有同名工具。
- public_name=`别名__工具名`；同时保留 server、remote_name、description（None 转空串）和 input_schema 的深拷贝。
- 后端路由应使用保存的映射，不靠拆分 public_name 猜 remote_name；远端工具名本身可以包含 `__`。
- 不修改传入描述。空输入返回 `[]`。

```bash
python -m pytest --run-exercises tests/mcp/test_level10_multiserver.py -q
```

完成标准：测试通过，展示两服务同名工具、连接一半失败、调用者异常和正常关闭四种情形。随后可以在此作用域里组合 Level 6 的分页发现和 Level 9 的适配器。

OAuth/授权服务器、远端部署、elicitation 与多轮请求、订阅、缓存一致性属于后续独立项目，不把本级命名空间或路径检查当成身份认证。
