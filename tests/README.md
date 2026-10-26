# 测试入口

所有命令在仓库根目录运行。默认 pytest 验证提供好的环境与设施，学生任务需要 --run-exercises 才执行；未实现时的 TODO 异常是预期现象。

| 目录 | 对应内容 | 验收命令 |
| --- | --- | --- |
| environment/ | 依赖、离线设施、流接口和MCP传输 | python -m pytest tests/environment -q |
| langchain/ | LangChain 1–10级与 L11 RAG 桥接 | python -m pytest --run-exercises tests/langchain -q |
| langgraph/ | LangGraph 1–10级 | python -m pytest --run-exercises tests/langgraph -q |
| rag/core/ | 手写核心10级与串联检查 | python -m pytest --run-exercises tests/rag/core -q |
| rag/workflows/ | 纠正检索工作流 | python -m pytest --run-exercises tests/rag/workflows -q |
| rag/graph/ | 图建模与多跳检索 | python -m pytest --run-exercises tests/rag/graph -q |
| mcp/ | MCP 1–10级 | python -m pytest --run-exercises tests/mcp -q |

RAG 机制只在 rag/core/ 验收一套实现；langchain/test_level11_rag_bridge.py 仅验证类型、消息与调用边界的适配。

每级统一使用 test_levelNN_主题.py，可单独运行；同一目录的集成测试使用 test_integration.py。pytest.ini 使用 importlib 导入模式，允许不同路径有同名测试文件。conftest.py 保留练习开关；rag/core/conftest.py 提供小样本构造器。

公开用例检查行为契约的一部分。绿色环境 CI 不代表练习完成或真实模型质量通过，仍需完成每级解释、边界自查和实验记录。仅安装 requirements-rag-core.txt 时，只运行 rag/core/；完整环境才可收集其他主题。

## 项目与迁移的验证范围

[curriculum/](../curriculum/README.md)的基础／迁移任务和[projects/](../projects/README.md)的阶段项目提供行为规格与人工评审矩阵，尚无预置实现或自动验收器；本目录的组件用例不会验收这些新增任务。学习者应在独立项目中编写测试，分别记录受控依赖、实际数据库、跨进程、容器与真实模型的验证范围。项目默认测试与需要实际模型的质量实验使用不同运行入口。

## 提供好的 MVP 示范程序

`python support/mvp_examples/run_all.py` 在隔离标准库子进程中执行七个示例，验证其内置行为断言；CI 单独运行这一入口，不计入 pytest 用例。它们是[配套读物](../curriculum/readings/README.md)的观察材料，不是学生练习答案或真实 HTTP／模型验收。

## C1 文件读取边界

[C1 测试](rag/core/test_level01_documents.py)区分 `.md` 普通文件、同后缀目录与命名管道，检查来源、排序、原文空白及空结果。`folder.md` 是普通文件时应读取，是目录时应忽略；目录排除不依赖特定名称。

命名管道用例使用真实的文件系统条目，并在读取入口设置失败探针，防止错误实现尝试读取时阻塞。系统或文件系统不支持命名管道时，该用例明确跳过；测试不额外约定符号链接行为。

## C2 文本切分边界

[C2 说明](../rag_practice/core/lessons/02_chunking.md)和[对应测试](rag/core/test_level02_chunking.py)分别验收窗口与段落，使用 `-k window` 或 `-k paragraph` 单独运行。预期值给出原文区间，比较完整 Chunk 的 text、source、ID 和偏移。

窗口用例覆盖默认无重叠、短尾、整除、大重叠、Unicode 和空白；段落用例覆盖完整分隔符预算、边缘空白、重复正文、超长段落，以及即使能与下一段合并也必须独立保留的短尾块。两部分均在空输入上检查非法参数，并验证输入与跨调用结果保持独立。
