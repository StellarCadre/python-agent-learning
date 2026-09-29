# ============================================================
# 高级类型注解
# ============================================================

from typing import (
    Literal, Final, TypedDict, Protocol, Generic, TypeVar,
    overload, ClassVar, Self,
)
from collections.abc import Iterable, Sequence, Mapping, Callable, Awaitable
import enum

# ---------- 1. Literal：限定具体取值 ----------
# 比 str 更精确，只能是列出的几个值

ModelName = Literal["gpt-4", "gpt-3.5", "claude"]
def chat(model: ModelName, prompt: str) -> str:
    return f"[{model}] {prompt}"

print(chat("gpt-4", "hi"))
# chat("其他模型", "x")               # 类型检查器报错

# 布尔/数字也可以 Literal
Mode = Literal["r", "w", "a"]
Status = Literal[200, 404, 500]

# ---------- 2. Final：真正的"常量"（类型检查层面）----------

MAX_SIZE: Final = 100
# MAX_SIZE = 200                      # mypy 报错（运行时仍可改）

# ---------- 3. Enum 枚举（Go 也有 enum 理念）----------

class Role(enum.Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

print(Role.USER, Role.USER.value)

def add_message(role: Role, content: str) -> dict:
    return {"role": role.value, "content": content}

print(add_message(Role.SYSTEM, "你是助手"))

# ---------- 4. TypedDict：带类型的 dict（结构固定）----------
# 比 dict[str, Any] 更精确，规定有哪些 key、什么类型

class ChatMessage(TypedDict):
    role: str
    content: str

msg: ChatMessage = {"role": "user", "content": "你好"}
print(msg)

# 可选字段
class ChatRequest(TypedDict, total=False):    # total=False 字段都可选
    model: str
    temperature: float
    messages: list[ChatMessage]

req: ChatRequest = {"model": "gpt-4"}

# ---------- 5. Protocol：结构化类型（类似 Go 接口，推荐）----------
# Go 接口隐式实现，Protocol 也是，不需要显式继承

class ToolProtocol(Protocol):
    name: str
    def run(self, query: str) -> str: ...

class SearchTool:                       # 没有继承 Protocol，但结构匹配
    name = "search"
    def run(self, query: str) -> str:
        return f"搜索 {query}"

def use_tool(tool: ToolProtocol) -> None:
    print(tool.run("python"))

use_tool(SearchTool())                 # 结构匹配即可

# ---------- 6. Iterable / Sequence / Mapping（collections.abc）----------

def total(nums: Iterable[int]) -> int:
    return sum(nums)

def first(items: Sequence[int]) -> int:
    return items[0]                    # Sequence 支持索引

def get_config(cfg: Mapping[str, str]) -> str:
    return cfg.get("model", "default")

print(total([1, 2, 3]))

# ---------- 7. 泛型 Generic / TypeVar ----------

T = TypeVar("T")

def first_item(items: list[T]) -> T | None:
    return items[0] if items else None

print(first_item([1, 2]))

# 泛型类
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

s: Stack[str] = Stack()
s.push("a")

# ---------- 8. overload 重载（多个签名）----------
# Go 不支持同名函数重载，Python 通过 overload 给类型检查器多个签名

@overload
def parse(value: str) -> str: ...
@overload
def parse(value: int) -> int: ...
def parse(value):
    return value

# ---------- 9. 异步类型 Awaitable / Callable ----------

AsyncFunc = Callable[[str], Awaitable[str]]

# ---------- 10. Self（Python 3.11+，链式方法注解）----------

class Builder:
    def add(self, text: str) -> Self:
        return self

# ---------- 11. ClassVar：区分类变量和实例变量 ----------

class Dog:
    species: ClassVar[str] = "犬科"     # 类变量
    name: str                          # 实例变量

    def __init__(self, name: str):
        self.name = name
