# HTTP 与模型调用的数据边界

前置：字典、字符串、字节和异常。目标：分清 HTTP 传输、模型接口格式、业务校验与内容质量。改编自 [MVP HTTP 基础及响应示例](SOURCES.md)；本篇不要求运行原来的模型客户端。

## 一次调用跨过哪些边界

```text
Python 数据 → JSON 文本 → UTF-8 字节 → HTTP 请求
HTTP 响应 → JSON 解析 → 接口字段检查 → 业务校验 → 内容评估
```

HTTP 描述方法、状态、字段和内容；`model`、`messages`、`choices` 属于具体模型接口。其他模型 API 可以使用不同 schema；“OpenAI-compatible”也不能保证各供应商所有特性一致。

模型服务是客户端的远端依赖；知识库 API 则是调用方访问你业务的入口。排查故障时先确认错误在哪一个边界发生。[HTTP 消息与语义](https://www.rfc-editor.org/rfc/rfc9110.html#section-6)

## 请求由什么组成

URL 的 scheme、主机、端口与路径决定访问目标；查询参数与片段是不同部分。GET 通常获取表示，POST 按接口约定处理提交的内容。具体接口选用的方法必须遵守其契约。

Content-Type 描述当前正文的媒体类型，不保证响应也采用相同格式。Authorization 承载认证信息，不会自行加密；HTTPS 提供传输保护，接收请求的服务仍能读取内容。示例与日志不应包含真实凭据。[HTTP 字段](https://www.rfc-editor.org/rfc/rfc9110.html#section-8.3)

Python 中的 `False` 与 `None` 经 JSON 序列化后分别为 `false` 与 `null`。`str(dict)` 使用 Python 对象表示，不能替代 JSON 序列化。需要自己构造字节正文时，`json.dumps` 得到文本，随后 UTF-8 编码得到字节；HTTP 客户端也可能提供自动 JSON 序列化接口。

`ensure_ascii=False` 影响非 ASCII 字符如何显示，不是加密。模型输入如果在 user content 中再保存一份 JSON 字符串，会形成内外两层结构，必须分别按契约解析。[Python JSON](https://docs.python.org/3.12/library/json.html)

## 响应成功需要逐层判断

HTTP 200 不保证响应正文是合法 JSON；JSON 合法不保证存在所需字段；字段齐全不保证结果符合业务约束；业务格式正确不保证结论可靠。收到空 choices、空白 content 或非法报告时，应在哪层失败需要明确说明。

连接、DNS、TLS 或本地超时可能发生在收到响应前，因此没有可用的 HTTP 状态码。本地 TimeoutError 不等于服务器返回了 504。反过来，收到 HTTP 错误响应也不意味着没有任何外部副作用发生。

同步／异步关心调用如何等待，流式／非流式关心结果如何交付；四种组合都需要各自实现。只修改 stream 参数，不能让原本按完整 JSON 解析的代码自动支持增量数据。

## 看一份有限的错误策略

运行 [http_contract.py](../../support/mvp_examples/http_contract.py)：

```bash
python support/mvp_examples/http_contract.py
```

程序人工构造成功与失败对象，并验证以下 MVP 政策：

| 情况 | 示例中的 HTTP 表达 | 附加语义 |
| --- | --- | --- |
| 请求非法 | 422 | 没开始业务执行 |
| 相同标识仍执行中 | 409 | 本次重复提交不调用依赖 |
| 本地容量已满 | 429 | 本次新提交未取得名额 |
| 上游供应商返回429 | 502/model_error | 不能与本地容量满载混淆 |
| 业务预算超时 | 504及细分错误码 | 明确哪个范围耗尽 |

这些映射是项目选择，知识库 API 需要自己公布策略，不能将表当作通用 HTTP 规范。具体状态语义查 [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#section-15)及 [429 定义](https://www.rfc-editor.org/rfc/rfc6585.html#section-4)。

失败对象保留已完成阶段，但 final_review 为空；私有错误正文不会进入公开响应。业务报告认为“证据不足”仍可以是一次正常完成的任务；系统无法提供合法结果才属于接口执行失败。

脚本没有建立网络连接，数字201只是人工构造策略。它没有验证真实 HTTP、框架路由、数据库或模型能力。真实接口需要另外运行服务与客户端测试。

## 转到知识库项目

在 [F3](../foundations/03_service.md)先定义 API 输入、输出与错误；在 [F4](../foundations/04_models.md)定义模型预算与失败。区分“无证据拒答”和“模型服务不可用”，并给客户端稳定的区分方法。

本篇补足调用边界，不包含 tokenizer、embedding 或生成模型的系统原理，也不包含 SQL。HTTP 服务的容量与关闭继续读[下一篇](04_service.md)。
