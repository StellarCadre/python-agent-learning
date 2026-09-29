# ============================================================
# 装饰器（Decorator）基础
# ============================================================
# 装饰器 = 在不修改原函数代码的前提下，给函数"包装"额外功能。
# 本质：一个接收函数、返回新函数的高阶函数。
#
# 语法糖 @decorator：
#   @log
#   def say(): ...
# 等价于：say = log(say)
#
# Agent 框架中到处是装饰器：@app.get、@tool、@property、@cached 等，
# 要求能看懂、会写简单装饰器。
# ============================================================

# ---------- 1. 从"手动包装"理解装饰器 ----------

def say_hello():
    return "hello"

# 定义一个装饰器：接收函数，返回包装后的函数
def add_logging(func):
    def wrapper():
        print(f"调用前：{func.__name__}")
        result = func()                # 调用原函数
        print(f"调用后，结果：{result}")
        return result
    return wrapper

# 手动包装（不用语法糖）
wrapped = add_logging(say_hello)
wrapped()

# ---------- 2. @ 语法糖 ----------

@add_logging
def say_bye():
    return "bye"

say_bye()                            # 自动被包装

# ---------- 3. 让包装函数支持任意参数（重要）----------
# 上面的 wrapper() 不能传参，用 *args/**kwargs 通用化

def universal_log(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] 调用 {func.__name__}, args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)   # 原样透传参数
        print(f"[LOG] {func.__name__} 返回 {result}")
        return result
    return wrapper

@universal_log
def add(a, b):
    return a + b

@universal_log
def greet(name, greeting="你好"):
    return f"{greeting}，{name}"

print(add(3, 5))
print(greet("Tom", greeting="嗨"))

# ---------- 4. functools.wraps（重要，修复元信息）----------
# 坑：包装后函数的名字/文档变成了 wrapper，丢失原函数信息

def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def documented():
    """这是重要文档"""
    return "x"

print(documented.__name__)           # wrapper（不是 documented！）
print(documented.__doc__)            # None（文档丢失）

# 修复：用 @functools.wraps(func)，把原函数元信息复制给 wrapper
import functools

def good_decorator(func):
    @functools.wraps(func)           # 必加，标准做法
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def documented2():
    """这是重要文档"""
    return "x"

print(documented2.__name__)          # documented2
print(documented2.__doc__)           # 文档保留

# ---------- 5. 计时装饰器（经典实用例子）----------

import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} 耗时 {elapsed:.6f} 秒")
        return result
    return wrapper

@timer
def slow_task():
    time.sleep(0.1)
    return "完成"

slow_task()

# ---------- 6. 多个装饰器叠加 ----------
# 从下往上应用（靠近函数的先包）

def decorator_a(func):
    @functools.wraps(func)
    def wrapper(*a, **k):
        print("A 前")
        r = func(*a, **k)
        print("A 后")
        return r
    return wrapper

def decorator_b(func):
    @functools.wraps(func)
    def wrapper(*a, **k):
        print("B 前")
        r = func(*a, **k)
        print("B 后")
        return r
    return wrapper

@decorator_a
@decorator_b
def target():
    print("原函数")

# 等价 target = decorator_a(decorator_b(target))
# 执行顺序像洋葱：A前 -> B前 -> 原函数 -> B后 -> A后
target()
