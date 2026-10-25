# Level 6：分页发现与有界遍历

**本级只解决：工具清单不止一页时，怎样完整读取并保证终止？**

完成 [level06_pagination.py](../level06_pagination.py) 的 list_all_tools(client, max_pages=20)。

- max_pages 是正整数，否则在调用客户端前抛 ValueError；它包含第一页。
- 首次 cursor 为 None，后续原样回传 next_cursor，不解析或修改它。
- 只有 next_cursor is None 表示结束；空字符串仍是合法的不透明 cursor。
- 按页面顺序收集 Tool，按工具名去重，保留首次出现的对象。不修改页面或描述。
- cursor 将重复请求时，或读满 max_pages 页仍未结束时，抛 PaginationError；最后允许的一页若结束则成功。
- 空页不等于结束。普通客户端异常直接传播。

```bash
python -m pytest --run-exercises tests/mcp/test_level06_pagination.py -q
```

测试注入固定分页客户端。MCPServer 默认返回一页；本题不是让你给 MCPServer 装饰器增加不存在的分页参数。实际自定义分页服务需用低层 server，见[官方分页说明](https://py.sdk.modelcontextprotocol.io/advanced/pagination/)。

下一步：[Level 7](07_execution.md)。
