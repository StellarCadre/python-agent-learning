# ============================================================
# asyncio 并发：gather / create_task / wait
# ============================================================
# Go 并发多个任务：多个 goroutine + sync.WaitGroup / errgroup
# Python 并发多个协程：
#   asyncio.gather(...)        并发并收集所有结果（最常用）
#   asyncio.create_task(...)   创建任务立即调度
# ============================================================

import asyncio
import time

async def fetch(name, delay, fail=False):
    await asyncio.sleep(delay)
    if fail:
        raise RuntimeError(f"{name}失败")
    return f"{name}结果"

# ---------- 1. 顺序 vs 并发对比 ----------

async def sequential():
    start = time.perf_counter()
    r1 = await fetch("A", 0.2)
    r2 = await fetch("B", 0.2)
    elapsed = time.perf_counter() - start
    print(f"顺序: {r1},{r2}, 耗时{elapsed:.2f}")   # 约0.4秒

async def concurrent():
    start = time.perf_counter()
    # gather 并发执行，等全部完成，结果按传入顺序返回
    r1, r2 = await asyncio.gather(
        fetch("A", 0.2),
        fetch("B", 0.2),
    )
    elapsed = time.perf_counter() - start
    print(f"并发: {r1},{r2}, 耗时{elapsed:.2f}")   # 约0.2秒

asyncio.run(sequential())
asyncio.run(concurrent())

# ---------- 2. gather 收集多个结果 ----------

async def many_tasks():
    results = await asyncio.gather(
        fetch("任务1", 0.1),
        fetch("任务2", 0.2),
        fetch("任务3", 0.15),
    )
    print("全部结果:", results)       # 顺序和传入一致

asyncio.run(many_tasks())

# gather 异常处理：return_exceptions=True 时异常作为结果返回（不中断其他）
async def with_errors():
    results = await asyncio.gather(
        fetch("好", 0.1),
        fetch("坏", 0.1, fail=True),
        fetch("好2", 0.1),
        return_exceptions=True,
    )
    print("含异常结果:", results)

asyncio.run(with_errors())

# 默认 return_exceptions=False，任一任务抛异常 gather 整体抛，
# 其他任务仍在后台运行但结果不收集

# ---------- 3. create_task ----------
# create_task 把协程包装成 Task 并立即开始调度（不用等 await）

async def task_demo():
    task1 = asyncio.create_task(fetch("T1", 0.2))
    task2 = asyncio.create_task(fetch("T2", 0.2))
    # 创建后已开始并发执行，这里可以做别的
    print("任务已启动，做其他事")
    r1 = await task1                 # 需要结果时 await
    r2 = await task2
    print(r1, r2)

asyncio.run(task_demo())

# gather 内部其实就是创建多个 task 再等待

# ---------- 4. 批量处理列表（实用）----------

async def fetch_all(items):
    tasks = [fetch(item, 0.1) for item in items]
    return await asyncio.gather(*tasks)     # * 解包列表

asyncio.run(fetch_all(["a", "b", "c"]))

# ---------- 5. asyncio.wait（更灵活，了解）----------

async def wait_demo():
    tasks = [
        asyncio.create_task(fetch("快", 0.1)),
        asyncio.create_task(fetch("慢", 0.3)),
    ]
    # 等待第一个完成
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    print("已完成:", [t.result() for t in done])
    # 取消剩余
    for t in pending:
        t.cancel()

asyncio.run(wait_demo())

# ---------- 6. 超时控制 timeout（Agent 调模型必备）----------

async def timeout_demo():
    try:
        result = await asyncio.wait_for(fetch("慢任务", 1.0), timeout=0.2)
        print(result)
    except asyncio.TimeoutError:
        print("超时了")

asyncio.run(timeout_demo())

# ---------- 7. 异步上下文管理器 ----------

async def context_demo():
    # async with 用于异步资源（如异步 HTTP 客户端、数据库连接）
    lock = asyncio.Lock()
    async with lock:                 # 自动获取/释放锁
        print("获得锁，安全操作")

asyncio.run(context_demo())

# ---------- 8. 信号量限流（控制并发数，实用）----------

async def limited_concurrency():
    sem = asyncio.Semaphore(2)        # 最多2个并发

    async def guarded(name):
        async with sem:
            return await fetch(name, 0.1)

    results = await asyncio.gather(*[guarded(f"T{i}") for i in range(5)])
    print("限流结果:", results)

asyncio.run(limited_concurrency())

# ---------- 9. Go 对比总结 ----------
#
#   Go                      Python
#   go f()                   asyncio.create_task(f())
#   WaitGroup.Wait           await asyncio.gather(...)
#   errgroup                 gather(return_exceptions)
#   select case              asyncio.wait / FIRST_COMPLETED
#   context.WithTimeout      asyncio.wait_for(..., timeout)
#   mutex.Lock/Unlock        async with asyncio.Lock()
#   带缓冲channel限流        asyncio.Semaphore
#
# 关键思维差异：
#   goroutine 是抢占式多线程，阻塞调用也能被调度；
#   Python 协程是协作式单线程，遇到 await 才切换，
#   协程里写阻塞代码（time.sleep、requests）会卡住所有任务！
#   异步代码中必须全程使用异步库（httpx 异步版、asyncio.sleep）。
