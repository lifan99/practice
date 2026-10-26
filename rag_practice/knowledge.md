# RAG 练习前置知识：C1 文档读取与 C2 文本切分

本页补充前两个手写练习需要的 Python 与文本处理知识。先读正在使用的主题，再回到任务独立实现；示例演示单项机制，不包含完整的文件加载器、窗口切分器或段落聚合实现。

| 当前练习 | 优先阅读 | 练习入口 |
| --- | --- | --- |
| C1 文档读取 | 数据对象、路径与文件类型、UTF-8、空白、列表与排序、异常 | [C1 任务](core/lessons/01_documents.md) |
| C2-A 窗口切分 | 字符与切片、循环控制、边界与不变量、输出开销 | [C2-A 任务](core/lessons/02_chunking.md#a重叠窗口) |
| C2-B 段落聚合 | 原文位置、正则匹配、连续区间预算 | [C2-B 任务](core/lessons/02_chunking.md#b段落聚合) |

本页使用手写核心的 `Document.text` 和 `Chunk`。框架类型转换集中在 [LangChain L11 桥接](../langchain_practice/lessons/11_rag_bridge.md)，使用同一套正文与偏移约定。下列 Python 代码块可在仓库根目录使用 Python 3.12 单独运行，不需要模型、数据库或网络。

## 1. Document、Chunk 与数据类

Document 表示一份带来源的完整文本；Chunk 表示其中的连续区间。前者用于保存输入，后者还需要定位依据，供后续检索和引用回溯。

```python
from rag_practice.core.types import Chunk, Document

document = Document(text="  示例\n", source="sample.md")
chunk = Chunk(
    chunk_id="sample.md:2:4",
    text="示例",
    source=document.source,
    start=2,
    end=4,
)
assert chunk.text == document.text[chunk.start:chunk.end]
assert chunk.source == document.source
```

两类对象已在 [core/types.py](core/types.py)中提供，用 `@dataclass(frozen=True)` 定义。dataclass 自动提供构造、显示和按字段比较等行为；关键字参数如 `text=...` 能明确每个值对应哪个字段，字段多时更便于核对。

`frozen=True` 限制字段重新赋值，不代替业务校验。`start: int` 也不会自动检查起止范围；调用代码和测试仍需保证正文、来源、位置与 ID 的一致性。[Python 数据类说明](https://docs.python.org/3.12/library/dataclasses.html)

例如同一个 source 下，正文都是 `aa` 的两个块，也可能分别来自 `[0,2)` 和 `[4,6)`；正文相同不代表它们是同一个块。

## 2. Path 是路径对象

`Path` 保存路径并提供相关操作。构造路径对象不会创建文件；使用 `/` 可以拼接路径，`.name`、`.stem` 和 `.suffix` 用来观察名称。

```python
from pathlib import Path

path = Path("materials") / "report.v2.md"
assert path.name == "report.v2.md"
assert path.stem == "report.v2"
assert path.suffix == ".md"
assert Path("report.md.bak").suffix == ".bak"
```

相对路径从当前工作目录解释，而不是自动相对于 Python 文件。因而相同的 `Path("materials")` 在不同启动目录可能指向不同位置。排查路径问题时，可以观察 `Path.cwd()` 与 `path.resolve()`；得到绝对路径不代表它实际存在。

### 2.1 属性与方法：什么时候要括号

| 表达式 | 得到什么 |
| --- | --- |
| `path.name` | 文件系统条目的名字字符串 |
| `path.suffix` | 最后一个扩展名字符串 |
| `path.exists()` | 执行存在性检查，返回 bool |
| `path.is_dir()` | 执行目录检查，返回 bool |
| `path.is_file()` | 执行普通文件检查，返回 bool |
| `path.is_file` | 方法对象本身，尚未执行检查 |

`if path.is_file:` 检查的是方法对象的真假值；普通的绑定方法对象为真，不能据此判断路径类型。

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as temporary:
    missing = Path(temporary) / "missing.md"
    assert missing.exists() is False
    assert callable(missing.is_file)
    assert bool(missing.is_file) is True
    assert missing.is_file() is False
```

### 2.2 文件名和文件类型分别判断

文件和目录都可以使用带扩展名的名称。`folder.md` 只是名字，是否能按普通文本文件读取，要看实际条目类型。

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as temporary:
    root = Path(temporary)
    directory = root / "chapter.md"
    directory.mkdir()
    file = root / "folder.md"
    file.write_text("正文", encoding="utf-8")

    assert directory.suffix == file.suffix == ".md"
    assert directory.is_dir() and not directory.is_file()
    assert file.is_file() and not file.is_dir()
```

“不是目录”也不能保证“是普通文件”，例如命名管道具有另一种文件类型。C1 的契约要求读取普通文件，筛选应表达这个正面要求。本级不扩展符号链接策略。

### 2.3 本层遍历与递归遍历

- `directory.iterdir()` 枚举直接子项，包括文件和目录。
- `directory.glob("*.md")` 按模式选择本层名称；匹配结果仍可能是目录。
- `directory.rglob("*.md")` 递归查找，搜索范围包含子目录。

glob 的默认大小写匹配方式与平台有关；C1 要求后缀严格等于 `.md` 时，需要遵守这个显式字符串条件，不能把某个平台上的 glob 行为当作全部规则。[Python pathlib 说明](https://docs.python.org/3.12/library/pathlib.html)

## 3. UTF-8：从磁盘字节到 Python 字符串

磁盘保存字节，`read_text(encoding="utf-8")` 按 UTF-8 解码并返回 str。编码名称属于接口参数，拼写错误会造成独立的错误；没有正确解码，后续字符位置就无从谈起。

```python
text = "中文"
encoded = text.encode("utf-8")
assert isinstance(encoded, bytes)
assert len(text) == 2
assert len(encoded) == 6
assert encoded.decode("utf-8") == text
```

字符数和字节数不同。C2 的 start／end 指向解码后的 Python 字符串；不能拿 UTF-8 字节坐标切这个字符串。

文本模式还可能进行换行转换。C1 的“原文”以读取后的字符串为准，任务没有要求逐字节保留 CRLF。

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as temporary:
    path = Path(temporary) / "line.txt"
    path.write_bytes(b"A\r\nB")
    assert path.read_text(encoding="utf-8") == "A\nB"
```

非法 UTF-8 与“空文件”是不同情况。前者意味着无法按约定解码，C1 要求传播解码错误；后者是可以成功读取的空字符串。

## 4. 空字符串、空白与不可变字符串

`""` 没有字符；`" \t\n"` 包含空格、制表符和换行，长度大于0。两者在“是否有非空白正文”这个问题上都可以被视为空，但不能用长度为0覆盖所有空白情况。

```python
empty = ""
whitespace = " \t\n"
raw = "  alpha\n\nbeta  \n"
cleaned = raw.strip()

assert not empty
assert bool(whitespace)
assert whitespace.strip() == ""
assert cleaned == "alpha\n\nbeta"
assert raw == "  alpha\n\nbeta  \n"
```

Python 字符串不可变，strip 返回处理后的字符串值，不会原地改写 raw。若把处理后的值重新赋给 raw，变量才会转而指向这个结果。strip 只移除首尾空白，不删除正文内部的空行；lstrip 和 rstrip 分别处理左侧和右侧。

C1 用清理后的结果判断是否有正文，再按契约保存读取到的字符串。C2-A 保留窗口边缘空白；C2-B 根据有效段落选择原文区间。判断规则和保存规则需要分别理解。[Python 字符串方法](https://docs.python.org/3.12/library/stdtypes.html#string-methods)

## 5. 列表、追加与确定性顺序

列表下标只能访问或替换已有位置。空列表还没有第0项，不能靠赋值到下标创建它；append 会向末尾增加一个元素。

```python
values = []
result = values.append("first")
values.append("second")
assert values == ["first", "second"]
assert result is None
```

append 修改列表并返回 None，因此 `values = values.append(...)` 会让变量丢掉原先的列表引用。收集多个 Document 或 Chunk 时，需要区分“修改容器”和“取得一个返回值”。

文件系统枚举不保证所需的文件名顺序。sorted 返回一个新列表；字符串按字典序比较，数字形式的名字也仍是字符串。

```python
names = ["b.md", "2.md", "a.md", "10.md"]
ordered = sorted(names)
assert ordered == ["10.md", "2.md", "a.md", "b.md"]
assert names == ["b.md", "2.md", "a.md", "10.md"]
```

对路径排序时，要确认比较的是任务指定的文件名规则。固定顺序有助于重现结果，也让测试能直接比较列表；不能依赖条目的创建时间。

## 6. 字符索引与左闭右开切片

对于 `ABCDE`，字符索引依次是0到4。切片 `[start:end]` 包含 start，排除 end，合法区间的长度为 `end - start`。

```python
text = "ABCDE"
assert text[1:4] == "BCD"
assert len(text[1:4]) == 4 - 1
assert text[:2] == "AB"
assert text[2:] == "CDE"
assert text[2:2] == ""
```

相邻的 `[0,2)` 和 `[2,5)` 能拼回原文，不会遗漏或重复中间字符；重叠窗口则有意让相邻区间共享一部分字符。无论采用哪种切分，Chunk.text 都应与其保存的原文区间一致。

Python 对越界切片比较宽容，这不代表 Chunk 可以保存越界的 end：

```python
text = "ABCDE"
assert text[1:99] == "BCDE"
assert text[4:2] == ""
assert len(text) == 5
```

切片能运行只是语言行为；C2 还要求非空块满足 `0 <= start < end <= len(text)`，并且元数据与实际切片一致。

### 6.1 Unicode 位置、空白与重复正文

Python str 的索引按 Unicode 码点计算；一个屏幕上显示的符号不一定只有一个码点，中文和 emoji 也不能按 UTF-8 字节长度计算。

```python
text = "A😀中B"
assert len(text) == 4
assert text[1:3] == "😀中"
assert len("e\u0301") == 2
```

同样，删除前导空白会改变后续文字的坐标。重复正文也不能仅凭内容决定位置：

```python
raw = "  cat cat\n"
assert raw[2:5] == raw[6:9] == "cat"
assert raw.find("cat") == 2
assert raw.strip().find("cat") == 0
```

find 默认返回第一次匹配的位置；C2 必须区分上述两个区间。保留原文、显式记录位置，是后续引用回溯的基础。

## 7. for、while 与控制流

for 逐项处理一个可迭代对象；while 在每次进入循环体前判断条件。range 的终点不包含在结果中，第三个参数是步长。

```python
assert list(range(2, 7, 2)) == [2, 4, 6]
assert list(range(0, 0)) == []
```

| 语句 | 作用范围 | 当前迭代后面的语句是否执行 |
| --- | --- | --- |
| `continue` | 结束当前迭代，转向下一次迭代的条件检查或取值 | 不执行 |
| `break` | 退出最内层循环，继续循环后面的代码 | 不执行 |
| `return` | 结束整个函数并返回 | 不执行函数内后续代码 |

```python
numbers = [1, -1, 2]
kept = []
for number in numbers:
    if number < 0:
        continue
    kept.append(number)
assert kept == [1, 2]

prefix = []
for number in numbers:
    if number < 0:
        break
    prefix.append(number)
assert prefix == [1]
```

在 while 中使用 continue 时，需要确认相关状态仍会更新，否则可能不断进入同一轮条件。C2-A 的循环需要同时满足参数有效、起点推进和到达末尾后结束；具体输出条件以任务契约为准。

### 7.1 记录不变量与执行轨迹

不变量是每次检查某个程序位置时都应成立的性质。例如，构造完一个块后，可以核对正文是否等于原文切片、偏移是否有效、来源是否保持一致。

调试时给变量命名为 text、start、end、step 或 chunks，通常比 t、i、c 更容易解释。先用短输入写出预期区间，再逐轮记录“进入循环时的状态、生成的区间、更新后的状态”，寻找第一次出现差异的位置。变量更新前和更新后的含义不能混用。

## 8. 正则表达式与匹配位置

C2-B 的段落分隔符为 `\n[ \t]*\n`。理解它需要区分 Python 字符串字面量和正则引擎的语法。

| 正则部分 | 含义 |
| --- | --- |
| `\n` | 一个换行符 |
| `[ \t]` | 一个空格或制表符 |
| `*` | 前面的模式出现0次或多次 |

因此两个换行可以直接相邻，也可以在中间包含空格或制表符；单个换行、夹有非空白正文的两行不符合这个分隔符。

```python
import re

pattern = r"\n[ \t]*\n"
assert re.fullmatch(pattern, "\n\n") is not None
assert re.fullmatch(pattern, "\n \t\n") is not None
assert re.fullmatch(pattern, "\n") is None
assert re.fullmatch(pattern, "\nX\n") is None
```

原始字符串 `r"\n"` 保存反斜杠和字母 n，正则引擎再把这个模式解释为换行匹配；普通字符串 `"\n"` 在 Python 字面量阶段就表示换行。

split 可以取得分割后的文本；需要原始匹配位置时，Match 对象的 start、end 或 span 方法能表达对应区间。下面用数字匹配观察这个接口，不包含段落切分实现：

```python
import re

text = "x12 y345"
matches = list(re.finditer(r"\d+", text))
assert [(match.group(), match.span()) for match in matches] == [
    ("12", (1, 3)),
    ("345", (5, 8)),
]
assert all(text[match.start():match.end()] == match.group() for match in matches)
```

finditer 按顺序返回非重叠匹配。分隔符的匹配区间属于原文中的间隔，不能直接当作有效段落或最终 Chunk；需要按 C2-B 的契约独立处理空白、区间和预算。[Python re 说明](https://docs.python.org/3.12/library/re.html)

## 9. 连续区间预算与输出开销

多个片段的正文长度之和，不一定等于覆盖它们的连续原文区间长度。只要 Chunk.text 要保持原文切片，中间的分隔符和空白也会占用预算。

```python
text = "red\n\nblue"
assert len("red") + len("blue") == 7
assert len(text[0:9]) == 9
assert text[0:9] == "red\n\nblue"
```

C2-B 的 max_chars 约束连续区间，不能通过删除中间空白来凑预算。超长段落拆出的小尾块是否能与下一段合并，则由任务的明确规则决定；它不是仅凭“还放得下”就能判断的问题。

复杂度也需要区分扫描输入和产生输出。在常用的 CPython 实现中，len(str) 为常数时间；正文切片通常涉及复制，与输出长度有关。即使循环次数不多，大量重叠也可能生成很多重复文本。

分析时可以分别记原文长度 n、块数 k，以及输出正文和 ID 字符串的总长度 L，检查排序、扫描、对象构造和字符串复制的成本。C1 的排序还与候选文件数量有关；C2 的时间和额外空间需要计入实际输出，不能一概按原文长度估算。字符预算也不能直接充当 tokenizer 的 token 预算。

## 10. 异常、测试与学习顺序

异常把“不能按契约完成请求”与“正常得到空结果”区分开。空目录可以返回空列表，路径不存在需要报告错误；文本读取失败不能伪装成没有有效文档。

| 情况 | 对应概念 | 练习要求 |
| --- | --- | --- |
| 路径不存在 | `FileNotFoundError` | C1 报告路径错误 |
| 输入路径是普通文件而不是目录 | `NotADirectoryError` | C1 不把它当作单文件请求 |
| 非法 UTF-8 | `UnicodeDecodeError` | C1 向调用方传播 |
| 大小／重叠范围非法 | `ValueError` | C2 即使输入为空也要校验 |
| 有效输入没有可返回内容 | 正常空结果 | 按各题规则返回 `[]` |

raise 创建失败分支；try／except 处理特定失败。宽泛捕获异常再返回 `[]` 会让错误与正常空结果混在一起。调试时先读 traceback 最后给出的异常类型和消息，再回到自己代码中最早违反契约的位置。

回到任务后，按以下顺序验收：

```bash
python -m pytest --run-exercises tests/rag/core/test_level01_documents.py -q
python -m pytest --run-exercises tests/rag/core/test_level02_chunking.py -k window -q
python -m pytest --run-exercises tests/rag/core/test_level02_chunking.py -k paragraph -q
```

pytest 的 `-k` 根据测试名称筛选用例；`--run-exercises` 是本仓库启用练习验收的开关。阅读和运行示例之后，使用自己的实现完成练习，再用新的边界输入检查迁移能力。更一般的校验分层与依赖替换可继续阅读[契约与依赖](../curriculum/readings/01_contracts.md)。
