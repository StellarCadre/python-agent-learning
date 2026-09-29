# ============================================================
# dataclass 数据类（Agent 开发高频，推荐）
# ============================================================
# Go 写数据结构：type User struct { Name string; Age int }
# Python 普通类要在 __init__ 里手写赋值，字段多了很啰嗦。
# @dataclass 自动生成 __init__、__repr__、__eq__ 等，
# 专门用来写"以存数据为主"的类，非常方便。
# ============================================================

from dataclasses import dataclass, field, asdict, astuple
from typing import Optional

# ---------- 1. 基本 dataclass ----------

@dataclass
class Point:
    x: int
    y: int

# 自动生成 __init__：Point(x, y)
p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)

print(p1)                            # Point(x=1, y=2)，自动生成 __repr__
print(p1 == p2)                      # True，自动生成 __eq__（按字段比较）
print(p1 == p3)

# ---------- 2. 默认值 ----------

@dataclass
class User:
    name: str
    age: int = 18                     # 默认值
    email: Optional[str] = None       # 可空
    active: bool = True

u1 = User("Tom")
u2 = User("Bob", 20, "b@c.com")
print(u1, u2)

# 坑：和函数参数一样，默认值不能用可变对象（list/dict）
# 要用 field(default_factory=...)

# ---------- 3. field：复杂字段配置 ----------

@dataclass
class Article:
    title: str
    tags: list[str] = field(default_factory=list)          # 每个实例独立的空列表
    metadata: dict = field(default_factory=dict)
    views: int = field(default=0)

    # 不参与比较/打印的字段
    internal_id: int = field(default=0, repr=False)

    # 只读字段（初始化后不能改）
    uuid: str = field(default="id-xxx", repr=True)

a1 = Article("第一篇")
a1.tags.append("python")
a1.metadata["author"] = "Tom"
print(a1)

a2 = Article("第二篇")
print(a2.tags)                       # []（独立，不受 a1 影响）

# ---------- 4. frozen 不可变 dataclass ----------

@dataclass(frozen=True)
class Config:
    model: str
    temperature: float = 0.7

cfg = Config("gpt-4")
# cfg.model = "gpt-3.5"              # 报错！frozen 后只读
# frozen dataclass 可以做 dict 的 key（可哈希）

# ---------- 5. 转换 ----------

@dataclass
class Product:
    pid: int
    name: str
    price: float

prod = Product(1, "书", 29.9)
print(asdict(prod))                  # 转 dict
print(astuple(prod))                 # 转 tuple

# ---------- 6. 后初始化处理 __post_init__ ----------

@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)  # 不放入 __init__ 参数，自动计算

    def __post_init__(self):
        # __init__ 赋值后自动调用，适合计算派生字段、校验
        self.area = self.width * self.height

r = Rectangle(3, 4)
print(r.area)

# 校验例子
@dataclass
class Percent:
    value: float

    def __post_init__(self):
        if not (0 <= self.value <= 100):
            raise ValueError(f"百分比必须在0~100，收到 {self.value}")

try:
    Percent(150)
except ValueError as e:
    print(e)

# ---------- 7. 实战：Agent 消息与配置 ----------

@dataclass
class Message:
    role: str                         # system/user/assistant
    content: str

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class ChatConfig:
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    stream: bool = False

@dataclass
class ChatRequest:
    messages: list[Message] = field(default_factory=list)
    config: ChatConfig = field(default_factory=ChatConfig)

req = ChatRequest(
    messages=[
        Message("system", "你是助手"),
        Message("user", "你好"),
    ],
    config=ChatConfig(temperature=0.2),
)
print(req)
print([m.to_dict() for m in req.messages])

# ---------- 8. dataclass vs Pydantic BaseModel ----------
# dataclass：标准库，轻量，适合内部数据结构，不做运行时类型强校验
# Pydantic：第三方库，自动运行时校验/序列化，FastAPI 用它
# Agent 内部传数据用 dataclass 很合适，接口边界用 Pydantic
