# RAG 手写主线

先用 Python 解释并实现检索机制，再接框架。十级任务全部使用本包的 dataclass 与普通函数，**不导入 LangChain、LangGraph 或任何向量数据库**。允许标准库和可选 NumPy；不得用现成检索器、BM25／排序指标库替代本级要求的计算。模型训练不在本路径内，embedding、生成、分词、重排模型通过回调注入。

任务保留 TODO，不附答案。前置：Python 函数、列表、字典、集合、异常、dataclass；第 3 级起需要向量、范数、点积，第 5 级需要词频与文档频率，第 7 级需要对数和均值。无需先学 LangChain。

| 级别 | 需要亲手实现的能力 | 任务 | 代码 |
| --- | --- | --- | --- |
| C1 | 文件读取与来源 | [契约](lessons/01_documents.md) | [代码](exercises/level01_documents.py) |
| C2 | 重叠窗口、段落聚合、原文偏移 | [契约](lessons/02_chunking.md) | [代码](exercises/level02_chunking.py) |
| C3 | 余弦相似度、精确 Top-k | [契约](lessons/03_vectors.md) | [代码](exercises/level03_vectors.py) |
| C4 | 自有索引、embedding 快照、检索前过滤 | [契约](lessons/04_index.md) | [代码](exercises/level04_index.py) |
| C5 | BM25 词法检索 | [契约](lessons/05_bm25.md) | [代码](exercises/level05_bm25.py) |
| C6 | 上下文、普通函数问答、空结果拒答 | [契约](lessons/06_pipeline.md) | [代码](exercises/level06_pipeline.py) |
| C7 | Recall、MRR、NDCG 与固定集评估 | [契约](lessons/07_metrics.md) | [代码](exercises/level07_metrics.py) |
| C8 | chunk 级 RRF 与双路融合 | [契约](lessons/08_hybrid.md) | [代码](exercises/level08_hybrid.py) |
| C9 | 重排、完整上下文 token 预算 | [契约](lessons/09_context.md) | [代码](exercises/level09_context.py) |
| C10 | 有界多查询扩展与排名融合 | [契约](lessons/10_multiquery.md) | [代码](exercises/level10_multiquery.py) |

C1→C2→C4，C3→C4；C5 与 C4 可并行学习；C6 接任意 retriever；C7 建立评估基线后再做 C8–C10。测试使用独立输入，可单独验收每一级；组合题通过注入替代组件隔离尚未完成的前级。提供好的 [types.py](types.py) 只定义数据契约。

## 安装与运行

在仓库根目录，用独立虚拟环境仅安装测试依赖即可运行这条路径：

```bash
python3 -m venv .venv-core
source .venv-core/bin/activate
python -m pip install -r requirements-rag-core.txt
python -m pytest --run-exercises tests/rag/core/test_level01_documents.py -q
python -m pytest --run-exercises tests/rag/core -q
```

完整 .venv 也可用；无需重复安装。没有 --run-exercises 时练习跳过；初始 TODO 失败是预期现象。仅安装最小依赖时，请只运行 tests/rag/core；其他主题和适配层需要总锁文件。NumPy 是可选实现工具，不是测试依赖。若创建 .venv-core，它受根目录 .gitignore 的 .venv* 规则保护。

## 共同契约与完成标准

- Document(text, source) 的正文保持原文；Chunk(chunk_id, text, source, start, end) 满足 text 等于对应 Document 的 text[start:end]，位置为 Python 字符索引、左闭右开。
- 除文件读取层之外，输入约定已经是正确类型；size、k 等参数均为整数，各级仍需校验其允许的数值范围。source 和 chunk_id 为非空单行字符串，正文可含中文；同 ID 的 chunk 内容与来源一致。
- 不修改输入；回调异常直接传播；有非法请求时，按本级约定在依赖调用前拒绝。公开测试没有覆盖全部契约，完成后自行增加反例。
- 每级需提交实现、测试结果，以及任务末尾要求的解释或实验记录。算法题另说明时间／空间复杂度；不以测试数量或组件数量代表模型质量。
- 允许调用模型或现成中文分词器，不要求重写 Transformer、embedding 训练或 cross-encoder。HNSW/IVF 属于完成精确检索后的选修。

最后完成[综合对比实验](experiments/README.md)，再进入 [LangChain 适配层](../langchain/README.md)。[RAG 总路径](../README.md)列出各分支和前置依赖。
