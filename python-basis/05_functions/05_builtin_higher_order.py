# ============================================================
# 内置高阶函数：map / filter / sorted / reduce / enumerate / zip
# ============================================================
# 高阶函数 = 接收函数作为参数，或返回函数的函数。
# Go 中可以传递函数，但没有内置这些工具，需要自己写。
# 注意：现代 Python 中 map/filter 很多场景被推导式替代，
#       sorted 仍然高频，reduce 用得较少。
# ============================================================

# ---------- 1. map(func, iterable) ----------
# 对序列每个元素应用函数，返回迭代器

nums = [1, 2, 3, 4, 5]

# 把每个数转字符串
str_nums = list(map(str, nums))
print(str_nums)                      # ['1','2','3','4','5']

# 多个序列（函数接收对应数量参数）
def add_two(a, b):
    return a + b
print(list(map(add_two, [1, 2, 3], [10, 20, 30])))  # [11,22,33]

# 等价推导式（更 Pythonic）
print([str(n) for n in nums])

# ---------- 2. filter(func, iterable) ----------
# 保留 func 返回 True 的元素

print(list(filter(lambda x: x > 3, nums)))   # [4,5]

# 过滤假值
values = [0, 1, False, 2, "", 3, None, 4]
print(list(filter(None, values)))    # None 作为函数表示保留真值 [1,2,3,4]

# 等价推导式
print([x for x in nums if x > 3])

# ---------- 3. sorted(iterable, key, reverse) ----------
# 返回排序后的新列表（原列表不变），这是最高频的高阶函数

data = [5, 2, 8, 1, 9]
print(sorted(data))                  # [1,2,5,8,9]
print(sorted(data, reverse=True))    # 降序
print(data)                          # 原列表不变

# key 函数
words = ["banana", "fig", "apple"]
print(sorted(words, key=len))        # 按长度

# 常用 key：operator.itemgetter / attrgetter
from operator import itemgetter, attrgetter

records = [
    {"name": "Tom", "age": 25},
    {"name": "Bob", "age": 20},
]
print(sorted(records, key=itemgetter("age")))
print(sorted(records, key=itemgetter("age"), reverse=True))

# 多级排序
students = [("Tom", 85), ("Bob", 90), ("Alice", 85)]
print(sorted(students, key=itemgetter(1, 0)))   # 先分数后名字

# ---------- 4. reduce（归约，在 functools 中）----------
# 把序列"累积"成一个值

from functools import reduce

# 求积
product = reduce(lambda acc, x: acc * x, [1, 2, 3, 4])
print(product)                       # 24

# 带初始值
sum_with_init = reduce(lambda acc, x: acc + x, [1, 2, 3], 100)
print(sum_with_init)                 # 106

# 实际开发中 sum/max/min/any/all 更直观，reduce 用于复杂归约

# ---------- 5. 其他常用内置工具 ----------

# enumerate：带索引（前面讲过）
for i, ch in enumerate("abc", 1):
    print(i, ch)

# zip：拉链
print(list(zip([1, 2, 3], ["a", "b", "c"])))

# all / any
print(all(x > 0 for x in [1, 2, 3]))
print(any(x > 5 for x in [1, 6, 3]))

# ---------- 6. itertools 模块（迭代工具，实用）----------

from itertools import chain, combinations, groupby, cycle, islice, permutations, product

# chain：扁平化串联多个可迭代对象
print(list(chain([1, 2], [3, 4], [5])))      # [1,2,3,4,5]

# groupby：分组（注意：需要先排序，连续相同才分到一组）
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
for key, group in groupby(data, key=lambda x: x[0]):
    print(key, list(group))

# combinations：组合
print(list(combinations([1, 2, 3], 2)))      # [(1,2),(1,3),(2,3)]

# permutations：排列
print(list(permutations([1, 2, 3], 2)))

# product：笛卡尔积
print(list(product([1, 2], ["a", "b"])))

# islice：切片迭代器（对生成器/无限序列有用）
print(list(islice(cycle("AB"), 5)))         # ['A','B','A','B','A']

# ---------- 7. 实战小例子 ----------

# 例子1：管道式数据处理
def pipeline(data, *funcs):
    """依次应用多个函数"""
    result = data
    for func in funcs:
        result = func(result)
    return result

raw = [1, 2, 3, 4, 5, 6, 7, 8]
step1 = lambda d: filter(lambda x: x % 2 == 0, d)
step2 = lambda d: map(lambda x: x * x, d)
step3 = lambda d: sorted(d, reverse=True)
print(pipeline(raw, step1, step2, step3))

# 例子2：计算加权平均
def weighted_average(values, weights):
    total = reduce(lambda acc, pair: acc + pair[0] * pair[1], zip(values, weights), 0)
    return total / sum(weights)

print(weighted_average([90, 80, 70], [0.5, 0.3, 0.2]))

# 例子3：Top N 排序
def top_n(items, n, key=None):
    return sorted(items, key=key, reverse=True)[:n]

articles = [{"title": "a", "views": 100}, {"title": "b", "views": 500}, {"title": "c", "views": 300}]
print(top_n(articles, 2, key=lambda x: x["views"]))
