# ============================================================
# 类型注解（Type Hints）基础
# ============================================================
# Go 是静态类型，类型是强制的，编译器检查。
# Python 类型注解是"可选提示"，运行时不强制，但：
#   1. IDE 能智能补全、提前发现错误
#   2. FastAPI/Pydantic 靠注解做校验和文档
#   3. 提高代码可读性和可维护性
# Agent 项目强烈建议写注解。
# ============================================================

# ---------- 1. 变量注解 ----------

# 基本类型
name: str = "Tom"
age: int = 18
height: float = 1.75
is_active: bool = True
nothing: None = None

# 容器类型（Python 3.9+ 推荐内置小写泛型）
numbers: list[int] = [1, 2, 3]
mapping: dict[str, int] = {"a": 1}
unique: set[str] = {"a", "b"}
pair: tuple[int, str] = (1, "a")

# 各种长度的 tuple
point2d: tuple[int, int] = (3, 4)
triple: tuple[int, str, bool] = (1, "x", True)
any_tuple: tuple[int, ...] = (1, 2, 3)    # ... 表示任意长度同类型

# 嵌套
matrix: list[list[int]] = [[1, 2], [3, 4]]
complex_map: dict[str, list[int]] = {"nums": [1, 2]}

# 注解后也可以不立即赋值（类似声明）
# config: dict[str, str]

# ---------- 2. 函数注解 ----------

def greet(name: str) -> str:
    return f"你好，{name}"

def add(a: int, b: int) -> int:
    return a + b

# 无返回值用 None
def log_message(msg: str) -> None:
    print(msg)

# 多参数默认值
def search(keyword: str, page: int = 1, page_size: int = 10) -> dict:
    return {"keyword": keyword, "page": page}

# *args/**kwargs 注解
def sum_all(*nums: int) -> int:
    return sum(nums)

def build(**options: str) -> dict:
    return options

# ---------- 3. typing 模块常用类型 ----------
# Python 3.10+ 很多可以用 | 运算符，老版本用 typing

from typing import Optional, Union, Any, List, Dict, Tuple, Set

# Optional[X] = X 或 None（可能为空）
def find_user(uid: int) -> Optional[str]:
    users = {1: "Tom"}
    return users.get(uid)              # 可能返回 None

# Python 3.10+ 等价写法：X | None
def find_user2(uid: int) -> str | None:
    return None

# Union：多种类型之一
def process(data: Union[int, str]) -> str:
    return str(data)

# Python 3.10+ 等价：int | str
def process2(data: int | str) -> str:
    return str(data)

# Any：任意类型（相当于不检查，少用）
def handle(data: Any) -> None:
    pass

# 老版本泛型写法（Python 3.8 及以前，了解）
old_list: List[int] = [1, 2]
old_dict: Dict[str, int] = {}
old_tuple: Tuple[int, int] = (1, 2)
old_set: Set[str] = set()

# ---------- 4. 容器值类型的注解 ----------

# dict 键值类型
scores: dict[str, float] = {"Tom": 90.5}

# list 中元素
users: list[dict[str, Any]] = [{"name": "Tom"}]

# ---------- 5. 类型别名（提高可读性）----------

# 给复杂类型起别名
JSON = dict[str, Any]
Vector = list[float]
UserId = int

def get_user(uid: UserId) -> JSON:
    return {"id": uid}

embedding: Vector = [0.1, 0.2, 0.3]

# Python 3.10+ 推荐 TypeAlias 显式声明
from typing import TypeAlias
ConfigDict: TypeAlias = dict[str, Union[str, int, bool]]

# ---------- 6. 注解不强制运行（再次强调）----------

def typed_add(a: int, b: int) -> int:
    return a + b

# 运行时传字符串不会报错（注解不检查）：
print(typed_add("a", "b"))            # ab（字符串拼接了！）
# 想要运行时校验用 Pydantic 或 mypy 静态检查

# 查看注解
print(typed_add.__annotations__)

# ---------- 7. 静态检查工具 mypy（了解）----------
# pip install mypy
# mypy your_file.py    # 像编译器一样检查类型错误
# Agent 项目可配合 mypy 提高质量，但非必须

# ---------- 8. 实战：Agent 相关注解 ----------

# 消息结构
Message = dict[str, str]

def build_messages(system: str, user_content: str, history: list[Message] | None = None) -> list[Message]:
    messages: list[Message] = [{"role": "system", "content": system}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_content})
    return messages

msgs = build_messages("你是助手", "你好")
print(msgs)

# 工具定义
ToolFunc = Any   # 实际可以用 Callable
from typing import Callable

# Callable[[参数类型], 返回类型]：注解函数类型
def register_tool(func: Callable[[str], str]) -> Callable[[str], str]:
    return func

def my_tool(query: str) -> str:
    return f"结果 {query}"

register_tool(my_tool)

# 无参数函数
Callback = Callable[[], None]
