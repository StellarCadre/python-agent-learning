# ============================================================
# 上下文管理器（Context Manager）与 with
# ============================================================
# with 用于保证资源的"获取/释放"成对出现，即使异常也能正确清理。
# Go 用 defer f.Close()，Python 用 with。
#
# 两种实现方式：
#   1. 类实现 __enter__ / __exit__
#   2. contextlib.contextmanager 装饰器 + yield（更简洁）
# ============================================================

# ---------- 1. 回顾 with 的使用 ----------
# with open("a.txt") as f:   # 结束自动 close
#     content = f.read()

# ---------- 2. 用类实现上下文管理器 ----------

class MyResource:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        # 进入 with 块时调用，返回值赋给 as 后的变量
        print(f"获取资源: {self.name}")
        return self                  # 通常返回自身

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 退出 with 块时调用（无论是否异常），负责清理
        print(f"释放资源: {self.name}")
        # 三个参数：异常类型、异常值、调用栈（无异常时都是 None）
        if exc_type is not None:
            print(f"块内发生异常: {exc_val}")
        # 返回 True 会"吞掉"异常；返回 False/None 异常继续传播（标准做法）
        return False

    def work(self):
        print(f"{self.name} 工作中")

with MyResource("数据库连接") as r:
    r.work()
# 退出时自动 __exit__

# 异常情况下也保证清理
try:
    with MyResource("连接2") as r:
        raise ValueError("块内出错")
except ValueError:
    print("异常已传播到外部，但资源已释放")

# ---------- 3. contextlib 装饰器方式（推荐，更简洁）----------

from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    # yield 之前 = __enter__（获取资源）
    print(f"打开 {name}")
    resource = {"name": name, "ready": True}
    try:
        yield resource               # yield 的值赋给 as 变量；暂停在这
    finally:
        # yield 之后 = __exit__（释放资源），放 finally 保证执行
        print(f"关闭 {name}")

with managed_resource("文件") as res:
    print("使用:", res)

# 异常处理版本
@contextmanager
def open_db(connection_str):
    conn = f"连接({connection_str})"
    print("建立", conn)
    try:
        yield conn
    except Exception as e:
        print("回滚事务:", e)
        raise                        # 异常继续传播
    finally:
        print("断开", conn)

try:
    with open_db("mysql://...") as db:
        print("执行SQL")
        raise RuntimeError("SQL错误")
except RuntimeError:
    pass

# ---------- 4. 常见内置上下文管理器 ----------

# 文件（最常见）
# with open(...) as f
# 锁
import threading
lock = threading.Lock()
with lock:
    print("线程安全区")

# 临时切换目录
from contextlib import suppress, redirect_stdout
import os, io

# suppress：忽略指定异常（替代 try/except pass）
with suppress(FileNotFoundError):
    os.remove("可能不存在的文件")
print("继续执行，文件不存在也不报错")

# ---------- 5. 异步上下文管理器（配合 async/await）----------

import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_connection():
    print("异步建立连接")
    try:
        yield "连接对象"
    finally:
        print("异步关闭连接")

async def main():
    async with async_connection() as conn:
        print("使用", conn)

asyncio.run(main())

# httpx.AsyncClient 就是用 async with 管理的

# ---------- 6. 实战：计时上下文管理器 ----------

import time

@contextmanager
def timer(label=""):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label} 耗时 {elapsed:.4f} 秒")

with timer("测试块"):
    time.sleep(0.1)
