# ============================================================
# lambda 匿名函数
# ============================================================
# Go 没有直接的匿名函数赋值简写，但 Go 有函数字面量：
#   square := func(x int) int { return x * x }
#
# Python lambda 语法：lambda 参数: 表达式
# 只能写一个表达式，不能写语句（不能有 if/for/赋值等，三元表达式可以）
# 主要用于"临时的小函数"，尤其作为 sorted/map/filter 的 key。
# ============================================================

# ---------- 1. lambda 基本用法 ----------

# 普通函数
def square_def(x):
    return x * x

# lambda 等价写法
square_lambda = lambda x: x * x

print(square_def(5), square_lambda(5))   # 25 25

# 多个参数
add = lambda a, b: a + b
print(add(3, 5))                     # 8

# 无参数
say_hi = lambda: "hello"
print(say_hi())

# 默认参数
greet = lambda name="Tom": f"hi {name}"
print(greet())
print(greet("Bob"))

# 条件表达式（类似三元）
is_even = lambda x: "偶数" if x % 2 == 0 else "奇数"
print(is_even(4))                    # 偶数

# ---------- 2. lambda 在排序中的应用（最常用场景）----------

pairs = [(1, "b"), (3, "a"), (2, "c")]

# 按第二个元素排序
pairs.sort(key=lambda x: x[1])
print(pairs)                        # [(3, 'a'), (1, 'b'), (2, 'c')]

# 按第一个元素降序
pairs.sort(key=lambda x: x[0], reverse=True)
print(pairs)

# dict 列表排序
users = [
    {"name": "Tom", "age": 25},
    {"name": "Bob", "age": 20},
    {"name": "Alice", "age": 30},
]
users.sort(key=lambda u: u["age"])
print(users)

# 多级排序
students = [("Tom", "A", 85), ("Bob", "B", 90), ("Alice", "A", 80)]
students.sort(key=lambda s: (s[1], -s[2]))   # 先按班级，再按分数降序
print(students)

# 字符串列表按长度排序
words = ["banana", "fig", "apple"]
words.sort(key=len)
print(words)                        # ['fig', 'apple', 'banana']

# ---------- 3. lambda 配合 map / filter ----------

nums = [1, 2, 3, 4, 5]

# map：对每个元素做变换
doubled = map(lambda x: x * 2, nums)
print(list(doubled))                 # [2,4,6,8,10]

# filter：过滤符合条件的元素
evens = filter(lambda x: x % 2 == 0, nums)
print(list(evens))                   # [2,4]

# 注意：现代 Python 更推荐用列表推导式代替 map/filter
print([x * 2 for x in nums])
print([x for x in nums if x % 2 == 0])

# ---------- 4. lambda 作为默认函数 / 回调 ----------

def transform(data, func=lambda x: x):
    """默认不做变换"""
    return [func(x) for x in data]

print(transform([1, 2, 3]))
print(transform([1, 2, 3], lambda x: x + 10))

# ---------- 5. lambda 的限制（坑）----------

# 1. 只能有一个表达式，不能写多条语句
# bad = lambda x: if x > 0: return "正"    # 语法错误

# 2. 不能赋值（但可以用海象运算符 :=，不推荐）
# 3. 复杂逻辑不要用 lambda，可读性差，应该用 def

# 坑：循环中创建 lambda 的闭包问题
functions = []
for i in range(3):
    functions.append(lambda: i)      # 三个 lambda 都引用同一个 i
print([f() for f in functions])      # [2,2,2]（循环结束 i=2）

# 修复：用默认参数立即绑定
functions2 = []
for i in range(3):
    functions2.append(lambda i=i: i)
print([f() for f in functions2])     # [0,1,2]

# ---------- 6. 实战小例子 ----------

# 例子1：简单计算器（dict 分发）
calculator = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b if b != 0 else None,
}
print(calculator["*"](4, 5))

# 例子2：数据清洗
raw = ["  Hello ", "WORLD", " Python "]
cleaned = list(map(lambda s: s.strip().lower(), raw))
print(cleaned)                       # ['hello', 'world', 'python']

# 例子3：根据规则提取
records = [
    {"id": 1, "score": 85},
    {"id": 2, "score": 45},
    {"id": 3, "score": 92},
]
# 及格的 id
passed_ids = list(map(lambda r: r["id"], filter(lambda r: r["score"] >= 60, records)))
print(passed_ids)                    # [1, 3]
# 推导式写法更清晰
print([r["id"] for r in records if r["score"] >= 60])
