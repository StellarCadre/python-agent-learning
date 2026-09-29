# ============================================================
# 推导式（Comprehensions）专门讲解
# ============================================================
# 推导式是 Python 的特色语法，用一行代码从一个序列生成新的序列，
# 比写 for 循环简洁很多，Agent 代码中非常高频。
#
# 三种推导式：
#   1. 列表推导式  [表达式 for ... if ...]
#   2. 字典推导式  {k:v for ... if ...}
#   3. 集合推导式  {表达式 for ... if ...}
# 另外还有生成器表达式（表达式 for ...），后面生成器章节讲。
# ============================================================

# ---------- 1. 列表推导式 ----------

# 基本语法：[表达式 for 变量 in 可迭代对象]

# 传统 for 循环写法
squares1 = []
for x in range(5):
    squares1.append(x * x) #将解析得到的0/1/2/3/4，分别作为一次列表所添加的元素
print(squares1)                      # [0, 1, 4, 9, 16]

# 列表推导式写法（等价，更简洁）
squares2 = [x * x for x in range(5)]  #用于填充列表数据
print(squares2)

# 带条件过滤：[表达式 for ... if 条件]
evens = [x for x in range(10) if x % 2 == 0]
print(evens)                        # [0, 2, 4, 6, 8]

# 对字符串操作
words = ["hello", "world", "python", "ai"]
lengths = [len(w) for w in words] #每从words中解析出一个，就将其保存到w中。再对该w进行各种处理
print(lengths)                      # [5, 5, 6, 2]

upper_words = [w.upper() for w in words]
print(upper_words)  # ["HELLO", "WORLD", "PYTHON", "AI"]

# 条件表达式（三元运算）放在结果位置
labels = ["偶数" if x % 2 == 0 else "奇数" for x in range(5)]
print(labels)                       # ['偶数', '奇数', '偶数', '奇数', '偶数']

# 嵌套循环的推导式
# 传统写法
pairs1 = []
for x in [1, 2]:
    for y in [3, 4]:
        pairs1.append((x, y))
print(pairs1)                       # [(1,3),(1,4),(2,3),(2,4)]

# 推导式写法
pairs2 = [(x, y) for x in [1, 2] for y in [3, 4]]
print(pairs2)

# 嵌套循环 + 条件
filtered = [(x, y) for x in range(3) for y in range(3) if x != y]
print(filtered)

# 嵌套列表推导式（处理矩阵）
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
# 转置矩阵
transposed = [[row[i] for row in matrix] for i in range(3)]
print(transposed)                   # [[1,4,7],[2,5,8],[3,6,9]]

# 坑：推导式不要写得太复杂，超过两层循环/多个条件时可读性差，
# 这时应该用普通 for 循环。


# ---------- 2. 字典推导式 ----------

# 基本语法：{键表达式: 值表达式 for ... in ...}

# 生成数字平方映射
square_map = {x: x * x for x in range(5)}
print(square_map)                   # {0:0, 1:1, 2:4, 3:9, 4:16}

# 两个列表合成 dict
keys = ["name", "age", "city"]
values = ["Tom", 18, "北京"]
d = {k: v for k, v in zip(keys, values)}
print(d)

# 过滤字典
scores = {"Tom": 85, "Bob": 45, "Alice": 92, "David": 58}
passed = {name: score for name, score in scores.items() if score >= 60}
print(passed)                       # {'Tom': 85, 'Alice': 92}

# 反转 key 和 value
original = {"a": 1, "b": 2, "c": 3}
reversed_d = {v: k for k, v in original.items()}
print(reversed_d)                   # {1: 'a', 2: 'b', 3: 'c'}
# 坑：反转要求 value 唯一且可哈希，否则会覆盖或报错

# 转换 key 大小写
config = {"Model": "gpt-4", "Temperature": 0.7}
lower_config = {k.lower(): v for k, v in config.items()}
print(lower_config)


# ---------- 3. 集合推导式 ----------

# 基本语法：{表达式 for ... in ...}

# 去重 + 变换
nums = [1, -1, 2, -2, 3, -3]
abs_values = {abs(x) for x in nums}
print(abs_values)                   # {1, 2, 3}

# 字符串中字符集合
chars = {ch for ch in "hello world" if ch != " "}
print(chars)


# ---------- 4. 生成器表达式 ----------
# 语法和列表推导式一样，但用圆括号：(表达式 for ...)
# 区别：列表推导式一次性生成所有元素（占内存），
#       生成器表达式惰性逐个生成（省内存）
# 大数据量时用生成器，后面生成器章节专门讲

# 计算总和时不需要先生成整个列表，直接用生成器表达式
total = sum(x * x for x in range(1000000))
print(total)

# 坑：只有一个参数时括号可以省略
# any(x > 0 for x in nums)

# list / dict / set 构造函数可以直接接收生成器表达式
result = list(x * 2 for x in range(5))
print(result)

# ---------- 5. 推导式中的作用域 ----------
# Python 3 中推导式有自己的作用域，循环变量不会泄漏到外部

x = "外部"
result = [x for x in range(3)]       # 这里的 x 是推导式内部的
print(x)                             # "外部"（外部 x 不受影响）
# Python 2 中会泄漏，Python 3 不会

# ---------- 6. 实战小例子 ----------

# 例子1：扁平化嵌套列表
nested = [[1, 2], [3, 4], [5]]
flat = [item for sublist in nested for item in sublist]
print(flat)                         # [1, 2, 3, 4, 5]

# 例子2：提取 dict 中符合条件的 key
data = {"gpt-4": 10, "gpt-3.5": 5, "claude": 8, "gpt-4-turbo": 12}
gpt_models = [k for k in data if k.startswith("gpt")]
print(gpt_models)

# 例子3：词频统计（字典推导式配合）
sentence = "the cat sat on the mat the cat"
words = sentence.split() #去除空格，变为thecatsatonthematthecat
freq = {w: words.count(w) for w in set(words)} #先转为集合进行去重，然后统计出现次数,并将结果放到字典中
print(freq)
