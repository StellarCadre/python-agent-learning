# ============================================================
# 异步编程 async / await 基础
# ============================================================
# Go 并发：goroutine（多线程调度）+ channel，runtime 自动管理，
#   go doTask()
#
# Python 异步：协程（coroutine）单线程事件循环，遇到 IO 主动挂起，
#   让出执行权给其他任务，IO 完成后再恢复。
#   async def 定义协程，await 等待异步结果。
#
# 为什么 Agent 要用异步？
#   调用大模型/网络是 IO 密集型，等待时间长，
#   异步可以单线程并发处理多个请求，提高吞吐。
# ============================================================

import asyncio

# ---------- 1. 定义和运行协程 ----------

# async def 定义协程函数，调用它不会立即执行，返回协程对象
async def say_hello():
    print("hello")
    return "完成"

# 直接调用只得到协程对象，不执行
coro = say_hello()
print(coro)                          # <coroutine object ...>

# 需要事件循环驱动，asyncio.run 是最简单入口
result = asyncio.run(say_hello())
print("返回:", result)

# 坑：
# 1. 协程必须通过 await 或 asyncio.run 运行，直接调用不执行
# 2. asyncio.run 一个线程只能有一个，通常在程序入口调用一次

# ---------- 2. await 等待 ----------

async def fetch_data(name, delay):
    print(f"{name} 开始，等待{delay}秒")
    await asyncio.sleep(delay)        # await 挂起，期间事件循环可跑其他任务
    print(f"{name} 结束")
    return f"{name}的数据"

async def main():
    # await 顺序执行：一个完成才下一个
    r1 = await fetch_data("任务1", 0.2)
    r2 = await fetch_data("任务2", 0.2)
    print(r1, r2)

asyncio.run(main())

# await 后面必须是"可等待对象"（协程、Task、Future）
# 普通同步函数/阻塞操作不能 await

# ---------- 3. 协程 vs 普通函数对比 ----------

def sync_blocking():
    import time
    time.sleep(0.2)                  # 阻塞整个线程

async def async_nonblocking():
    await asyncio.sleep(0.2)         # 挂起，不阻塞事件循环

# ---------- 4. asyncio.sleep vs time.sleep ----------
# time.sleep 会卡住整个事件循环（其他协程也跑不了）
# asyncio.sleep 才是异步等待，协程中必须用它

# ---------- 5. 协程返回值 ----------

async def compute(x):
    await asyncio.sleep(0.05)
    return x * 2

async def main2():
    result = await compute(21)
    print("结果:", result)

asyncio.run(main2())
