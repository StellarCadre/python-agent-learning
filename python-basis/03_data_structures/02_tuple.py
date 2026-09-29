# ============================================================
# tuple（元组）全面讲解
# ============================================================
# tuple 可以理解为"不可变的 list"。
# Go 中没有完全对应的类型，最接近固定长度的数组 [N]T。
# 特点：有序、不可变（创建后不能增删改）、允许重复、可以放任意类型。
#
# 为什么需要 tuple？
#   1. 不可变意味着安全，数据不会被意外修改
#   2. 可以作为 dict 的 key（list 不行）
#   3. 函数返回多个值本质就是 tuple
#   4. 比 list 稍省内存
# ============================================================

# ---------- 1. tuple 的多种创建方式 ----------

# 方式1：圆括号创建（最常见）
t1 = (1, 2, 3)
t2 = ("a", "b", "c")
t3 = (1, "hello", True, 3.14)        # 可以放不同类型
t4 = ()                              # 空元组

# 方式2：不加括号也可以（逗号才是 tuple 的标志，不是括号！）
t5 = 1, 2, 3
print(t5, type(t5))                  # (1, 2, 3) <class 'tuple'>

# 方式3：tuple() 构造函数
t6 = tuple([1, 2, 3])                # list -> tuple
t7 = tuple("abc")                    # 字符串 -> ('a', 'b', 'c')
t8 = tuple()                         # 空元组

# 单元素 tuple 的坑！必须加逗号
single1 = (42)                       # 这不是 tuple！括号被当普通括号
print(single1, type(single1))        # 42 <class 'int'>

single2 = (42,)                      # 这才是单元素 tuple，逗号不能少
print(single2, type(single2))        # (42,) <class 'tuple'>

single3 = 42,                        # 不加括号也要有逗号
print(single3, type(single3))        # (42,)

print(t1, t2, t3, t4, t6, t7)

# ---------- 2. 访问元素（和 list 完全一样）----------

fruits = ("apple", "banana", "cherry", "date")

print(fruits[0])                     # apple
print(fruits[-1])                    # date
print(fruits[1:3])                   # ('banana', 'cherry')
print(fruits[::2])                   # ('apple', 'cherry')
print(fruits[::-1])                  # ('date', 'cherry', 'banana', 'apple')

# ---------- 3. 不可变性（核心特性）----------

t = (1, 2, 3)
# t[0] = 100          # 报错 TypeError: 'tuple' object does not support item assignment
# t.append(4)         # 没有 append 方法
# t.remove(2)         # 没有 remove 方法
# del t[0]            # 不能删元素

# 但是！如果 tuple 里放了可变对象（如 list），那个 list 内部是可以改的
nested_t = (1, 2, [3, 4])
nested_t[2].append(5)                # tuple 里的 list 可以改
print(nested_t)                      # (1, 2, [3, 4, 5])
# 坑：tuple 不可变指的是"引用"不可变，引用指向的对象内部可变
# 这和 Go 数组里放 slice 指针类似


# ---------- 4. 解包（unpacking，tuple 最常用的场景）----------

# 基本解包
point = (3, 4)
x, y = point
print(x, y)                          # 3 4

# 函数返回多个值就是 tuple 解包
def get_user_info():
    return 1, "Tom", 25              # 本质返回 (1, "Tom", 25)

uid, uname, uage = get_user_info()
print(uid, uname, uage)

# 交换变量（本质也是 tuple 解包）
a, b = 1, 2
a, b = b, a                          # 右边先组成 tuple (2,1)，再解包
print(a, b)

# 解包时用 * 收集多余元素（Python 3）
numbers = (1, 2, 3, 4, 5)
first, second, *rest = numbers
print(first, second, rest)           # 1 2 [3, 4, 5]

first, *middle, last = numbers
print(first, middle, last)           # 1 [2, 3, 4] 5

*head, last2 = numbers
print(head, last2)                   # [1, 2, 3, 4] 5

# 用 _ 忽略不需要的值
uid2, _, uage2 = get_user_info()
print(uid2, uage2)

# 嵌套解包
data = (1, (2, 3), 4)
p, (q, r), s = data
print(p, q, r, s)                    # 1 2 3 4

# ---------- 5. tuple 的运算 ----------

# 拼接（创建新 tuple）
t1 = (1, 2)
t2 = (3, 4)
print(t1 + t2)                       # (1, 2, 3, 4)

# 重复
print(("a",) * 3)                    # ('a', 'a', 'a')

# 成员判断
print(2 in (1, 2, 3))                # True

# ---------- 6. tuple 的常用方法（只有2个，因为不可变）----------

t = (1, 2, 2, 3, 2, 4)

print(t.count(2))                    # 统计出现次数 3
print(t.index(3))                    # 查找索引 3 对应的值
# print(t.index(99))                # 找不到报 ValueError

print(len(t))                        # 长度 6

# ---------- 7. tuple 与 list 对比 ----------

# list 有但 tuple 没有的方法：append, extend, insert, remove, pop, clear, sort, reverse, copy
# tuple 只有：count, index
#
# list 用方括号 []，tuple 用圆括号 ()
# list 可变，tuple 不可变
# list 不能做 dict 的 key，tuple 可以（前提是元素都不可变）

# tuple 作为 dict 的 key（常用于坐标、复合键，类似 Go 中 struct 做 map key）
locations = {
    (39.9, 116.4): "北京",
    (31.2, 121.5): "上海",
}
print(locations[(39.9, 116.4)])      # 北京

# 坑：tuple 里如果有 list，就不能做 key
# bad_key = (1, [2, 3])
# d = {bad_key: "value"}   # TypeError: unhashable type: 'list'


# ---------- 8. 命名元组 namedtuple（了解，实用）----------
# 普通 tuple 只能用索引访问，namedtuple 可以用名字访问，类似轻量级的类

from collections import namedtuple

# 定义一个 Point 类型，有 x 和 y 两个字段
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)                      # 3 4（可以用属性名访问）
print(p[0], p[1])                    # 3 4（仍然可以用索引）
print(p)                             # Point(x=3, y=4)

# 实际开发中 dataclass 更常用（后面会讲），namedtuple 是老方案
