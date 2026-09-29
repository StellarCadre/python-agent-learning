# ============================================================
# set（集合）全面讲解
# ============================================================
# set 相当于 Go 中 map[T]struct{} 的用法，用于存储不重复的元素。
# 特点：可变、无序、元素不重复、元素必须可哈希（不可变类型）。
# frozenset 是不可变版本的 set。
#
# 主要用途：去重、集合运算（交集/并集/差集）、快速成员判断。
# ============================================================

# ---------- 1. set 的多种创建方式 ----------

# 方式1：花括号（注意和 dict 区分，set 没有冒号）
s1 = {1, 2, 3}
print(s1, type(s1))

# 方式2：set() 构造函数（创建空 set 只能用这个！）
empty = set()                        # {} 创建的是空 dict 不是空 set！
print(empty, type(empty))

s2 = set([1, 2, 2, 3, 3, 3])         # 从 list 创建，自动去重
print(s2)                            # {1, 2, 3}

s3 = set("hello")                    # 从字符串创建
print(s3)                            # {'h', 'e', 'l', 'o'}（无序，l去重）

# 方式3：集合推导式
s4 = {x for x in range(5)}
s5 = {x * x for x in [1, -1, 2, -2]}  # {1, 4}（平方后去重）

print(s4, s5)

# 元素必须是不可变类型（和 dict 的 key 一样）
# bad = {[1,2], [3,4]}    # TypeError: unhashable type: 'list'
valid = {1, "a", (1, 2)}             # int/str/tuple 可以

# ---------- 2. 添加元素 ----------

s = {1, 2, 3}

s.add(4)                             # 添加一个元素
print(s)                             # {1, 2, 3, 4}
s.add(2)                             # 添加已存在的元素，不报错也不变化
print(s)

s.update([5, 6, 7])                  # 批量添加
s.update({8, 9}, [10])               # 可以同时加多个可迭代对象
print(s)

# ---------- 3. 删除元素 ----------

s = {1, 2, 3, 4, 5}

s.remove(3)                          # 删除指定元素，元素不存在报 KeyError
print(s)
# s.remove(99)                       # KeyError

s.discard(99)                        # 删除元素，不存在也不报错（安全删除，推荐）
s.discard(4)
print(s)                             # {1, 2, 5}

val = s.pop()                        # 随机删除并返回一个元素（set 无序）
print("弹出:", val, "剩余:", s)

s.clear()                            # 清空
print(s)                             # set()

# ---------- 4. 成员判断 ----------
# set 的成员判断是 O(1)，list 是 O(n)，大数据量时 set 快很多

s = {1, 2, 3, 4, 5}
print(3 in s)                        # True
print(99 not in s)                   # True

# Go 中用 map[T]struct{} 做集合，判断 _, ok := set[x]
# Python 直接 in 即可

# ---------- 5. 集合运算（核心功能）----------

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# 交集：两个集合都有的元素
print(a & b)                         # {3, 4}
print(a.intersection(b))             # 等价写法

# 并集：两个集合所有元素（去重）
print(a | b)                         # {1, 2, 3, 4, 5, 6}
print(a.union(b))

# 差集：a 有但 b 没有
print(a - b)                         # {1, 2}
print(a.difference(b))
print(b - a)                         # {5, 6}

# 对称差集：只在其中一个集合出现（并集 - 交集）
print(a ^ b)                         # {1, 2, 5, 6}
print(a.symmetric_difference(b))

# ---------- 6. 集合关系判断 ----------

c = {1, 2}
d = {1, 2, 3, 4}

print(c <= d)                        # True，c 是 d 的子集
print(c.issubset(d))

print(d >= c)                        # True，d 是 c 的超集
print(d.issuperset(c))

print({1, 2} <= {1, 2})              # True（自己也是自己的子集）
print({1, 2} < {1, 2})               # False（真子集，必须严格小）

print(a.isdisjoint({9, 10}))         # True，两个集合是否没有交集

# ---------- 7. frozenset（不可变集合）----------

fs = frozenset([1, 2, 3])
print(fs, type(fs))
# fs.add(4)                          # 没有 add 方法，不可变

# frozenset 可以做 dict 的 key，普通 set 不行
# 也可以作为另一个 set 的元素
nested = {frozenset([1, 2]), frozenset([3, 4])}
print(nested)

# ---------- 8. 实际应用小例子 ----------

# 例子1：list 去重（最常见用途）
names = ["Tom", "Bob", "Tom", "Alice", "Bob"]
unique_names = list(set(names))
print(unique_names)                  # 去重，但顺序不保证
# Python 3.7+ 想保持顺序去重：
unique_ordered = list(dict.fromkeys(names))
print(unique_ordered)                # ['Tom', 'Bob', 'Alice']

# 例子2：找两个列表的共同元素
list_a = [1, 2, 3, 4, 5]
list_b = [4, 5, 6, 7, 8]
common = set(list_a) & set(list_b)
print(common)                        # {4, 5}

# 例子3：标签系统
user1_tags = {"python", "ai", "backend"}
user2_tags = {"python", "frontend", "design"}
print("共同兴趣:", user1_tags & user2_tags)
print("推荐标签:", user2_tags - user1_tags)

# 例子4：快速判断是否有重复
def has_duplicates(lst):
    return len(lst) != len(set(lst))

print(has_duplicates([1, 2, 3]))     # False
print(has_duplicates([1, 2, 1]))     # True
