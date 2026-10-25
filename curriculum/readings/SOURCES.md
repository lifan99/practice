# MVP 材料来源与改编说明

本课程的基础读物与离线示例改编自[多 Agent 审核 MVP（lifan99/utility，51d9f356）](https://github.com/lifan99/utility/tree/51d9f356e2a3c5bf27bff93aff2a7cf523a87232)。下表列出10份来源文件及其教学用途。源材料的本地修订为8d2e092f，所选文件与上述公开版本的 blob 哈希一致；版本与原始文件 SHA-256 记录在 [SOURCES.json](../../support/mvp_examples/SOURCES.json)。

| 原始文件 | 在本课程中的用途 |
| --- | --- |
| docs/technical/数据契约.md | 契约层次、类型与运行时规则、引用校验、quotes.py |
| docs/technical/异步.md | 顺序／并发、任务、预算、取消与所有权 |
| docs/technical/HTTP基础.md | 请求响应、JSON／字节、状态与模型接口边界 |
| docs/technical/服务.md | 分层、容量、活动去重、关闭与验证范围 |
| examples/core/E02_protocol.py | protocols.py：结构化协议和依赖替换 |
| examples/async/E01_concurrent_reviews.py | concurrency.py：事件探针与上下文隔离 |
| examples/async/E02_timeout_budgets.py | timeouts.py：预算作用域与错误分类 |
| examples/async/E03_cancel_cleanup.py | cancellation.py：取消传播和名额复用 |
| examples/api/E01_http_contract.py | http_contract.py：人工构造响应及公开错误 |
| examples/api/E02_admission_lifecycle.py | admission.py：准入与关闭顺序 |

## 改编方式与边界

读物按课程先修重组并改写，保留原设计的适用前提，增加对 RAG、P2 与迁移任务的连接；原项目中的路径和历史测试结论不迁入。六个独立脚本保留原行为，注释与 docstring 改成英文；protocols.py 增加两条断言。quotes.py 来自数据契约文中的小程序，增加重复正文观察。run_all.py 是新增的标准库验证入口。

原始材料中的参考答案、个人学习记录和完整项目实现不在这份复用清单内。讲解示例是提供好的阅读材料，不提供本课程独立迁移作业或知识库项目的完整解答。面试资料不得上传。

原服务的 HTTPX 0.28 依赖与课程 MCP 使用的 httpx2 分开维护。课程中的改编示例仅使用 Python 3.12 标准库，可独立于原服务、Streamlit 与供应商配置运行。

## 验证与局限

运行 `python support/mvp_examples/run_all.py` 会逐一执行七个示例并检查其行为断言；CI 使用同一入口。它验证受控本地行为，不能证明真实网络、模型质量、数据库事务、跨重启幂等或权限隔离。课程原有组件 pytest 与项目阶段验收继续独立呈现。
