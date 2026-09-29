# ============================================================
# 带参数的装饰器
# ============================================================
# 如果装饰器本身需要参数（如 @retry(3)、@cache(ttl=60)），
# 需要再套一层函数：
#   普通装饰器：接收函数，返回函数（2层）
#   带参装饰器：接收参数，返回一个"普通装饰器"（3层）
# ============================================================

import functools, time

# ---------- 1. 带参装饰器结构 ----------

def repeat(times):
    """让被装饰函数重复执行 times 次"""
    def decorator(func):             # 第2层：真正的装饰器
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for i in range(times):
                print(f"第{i+1}次执行")
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator                 # 第1层：返回装饰器

@repeat(3)                           # 注意有括号和参数
def say_hi(name):
    print(f"hi {name}")

say_hi("Tom")

# 理解：@repeat(3) 先执行 repeat(3) 得到 decorator，
# 再用 decorator 包装 say_hi

# ---------- 2. 重试装饰器（Agent 调 API 最实用）----------

def retry(max_attempts=3, delay=0.1, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    print(f"第{attempt}次失败: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay * attempt)   # 退避
            raise last_error
        return wrapper
    return decorator

call_count = 0
@retry(max_attempts=3, delay=0.05)
def unstable():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ConnectionError("网络错误")
    return "成功"

print(unstable())

# ---------- 3. 缓存装饰器（标准库自带，极常用）----------
# functools.cache / lru_cache 自动记忆化

from functools import cache, lru_cache

@cache                               # 无限缓存（Python 3.9+）
def fib(n):
    print(f"计算 fib({n})")
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(10))                       # 每个值只算一次
print(fib(10))                       # 直接返回缓存，不打印

@lru_cache(maxsize=128)              # 限制缓存数量
def expensive(n):
    return n * n

# ---------- 4. 类装饰器 ----------
# 装饰器也可以用类实现（靠 __call__）

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)   # 等价 wraps，保留元信息
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"第{self.count}次调用")
        return self.func(*args, **kwargs)

@CountCalls
def hello():
    return "hello"

hello()
hello()
print("总调用次数:", hello.count)

# ---------- 5. 装饰类（不只是函数）----------
# 装饰器也能装饰整个类（了解）

def add_repr(cls):
    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class Item:
    def __init__(self, name):
        self.name = name

print(Item("东西"))

# ---------- 6. 实战：注册机制（Agent 工具注册，非常实用）----------

# 用装饰器自动把函数注册到一个字典（框架常见模式）
TOOL_REGISTRY: dict = {}

def register_tool(name=None, description=""):
    def decorator(func):
        tool_name = name or func.__name__
        TOOL_REGISTRY[tool_name] = {
            "func": func,
            "description": description,
        }
        return func                  # 注册后原函数照常使用
    return decorator

@register_tool("search", "搜索网页")
def search_tool(query):
    return f"搜索: {query}"

@register_tool(description="查询天气")
def weather(city):
    return f"{city}: 晴"

print("已注册工具:", list(TOOL_REGISTRY.keys()))
print(TOOL_REGISTRY["search"]["func"]("python"))
