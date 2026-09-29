# ============================================================
# 生成器（Generator）
# ============================================================
# 普通函数用 return 返回一次结果；
# 生成器用 yield 逐个"产出"值，每次产出后暂停，下次继续。
#
# 好处：惰性计算，不一次性占内存，适合处理大数据/无限序列/流式输出。
# Agent 中 LLM 的流式（streaming）输出本质就是生成器模式。
# ============================================================

# ---------- 1. 最简单的生成器 ----------

def simple_gen():
    print("第一次")
    yield 1                          # 产出1并暂停
    print("第二次")
    yield 2
    print("第三次")
    yield 3

# 调用生成器函数得到生成器对象（不立即执行）
gen = simple_gen()
print(gen)

# next() 推进，执行到下一个 yield
print(next(gen))                     # 打印"第一次"，返回1
print(next(gen))                     # "第二次"，返回2
print(next(gen))                     # "第三次"，返回3
# print(next(gen))                   # 没有更多，抛 StopIteration

# 生成器通常直接用 for 遍历（自动 next 和处理结束）
for value in simple_gen():
    print("收到:", value)

# ---------- 2. 生成器 vs 列表（内存差异）----------

# 列表：一次性生成所有，占内存
def make_list(n):
    result = []
    for i in range(n):
        result.append(i)
    return result

# 生成器：需要时才算
def make_gen(n):
    for i in range(n):
        yield i

print(sum(make_gen(1000000)))        # 不占大量内存

# 生成器表达式（圆括号，前面讲过）
squares = (x * x for x in range(5))
print(list(squares))

# ---------- 3. yield 工作机制 ----------

def counter(start=0):
    n = start
    while True:                      # 无限生成器
        yield n
        n += 1

# 取前5个
gen = counter(10)
for _ in range(5):
    print(next(gen), end=" ")        # 10 11 12 13 14
print()

# ---------- 4. 生成器的方法 send / close（了解）----------

def echo_gen():
    while True:
        received = yield             # yield 可以接收 send 的值
        if received is None:
            break
        print("收到:", received)

g = echo_gen()
next(g)                              # 必须先启动到 yield
g.send("消息1")
g.send("消息2")
g.close()

# ---------- 5. yield from（委托生成器）----------
# 简化嵌套生成器

def chain(*iterables):
    for it in iterables:
        yield from it                # 等价于 for x in it: yield x

print(list(chain([1, 2], [3, 4], [5])))

# 扁平化嵌套结构
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

print(list(flatten([1, [2, [3, 4], 5], 6])))   # [1,2,3,4,5,6]

# ---------- 6. 实战小例子 ----------

# 例子1：读取大文件逐块处理
def read_in_chunks(path, chunk_size=1024):
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# 例子2：分页生成器（Agent 拉取数据常用）
def paginate_all(total, page_size):
    for offset in range(0, total, page_size):
        yield offset, min(offset + page_size, total)

print(list(paginate_all(25, 10)))

# 例子3：简单的流式文本（模拟 LLM streaming）
import time

def stream_response(full_text):
    """模拟模型逐字返回"""
    for ch in full_text:
        time.sleep(0.02)
        yield ch

# 实际异步场景用 async for，这里同步演示
full = ""
for ch in stream_response("你好，世界"):
    full += ch
print("拼接完整:", full)

# 例子4：斐波那契无限生成
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
print([next(fib) for _ in range(10)])
