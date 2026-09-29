# ============================================================
# 函数基础
# ============================================================
# Go 定义函数：
#   func add(a int, b int) int { return a + b }
#
# Python 定义函数：
#   def add(a, b):
#       return a + b
#
# def 是 define 的缩写，不需要声明参数和返回值类型（可以加注解）。
# ============================================================

# ---------- 1. 基本函数定义与调用 ----------

def greet():
    """无参数无返回值的函数"""
    print("你好")

greet()

def add(a, b):
    """两个参数，有返回值"""
    return a + b

result = add(3, 5)
print(result)                        # 8

# 文档字符串 docstring：函数体第一行的字符串，用来说明函数用途
# 可以通过 help(函数名) 或 函数名.__doc__ 查看
help(add)                            # 显示文档
print(greet.__doc__)

# Go 用注释 // Add ... 说明，Python 推荐用 docstring

# ---------- 2. 返回值 ----------

# 没有 return 默认返回 None
def do_nothing():
    pass

print(do_nothing())                  # None

# return 可以提前结束函数（Go 也一样）
def check_positive(n):
    if n <= 0:
        return "非正数"
    return "正数"

# 返回多个值（本质是 tuple）
def get_min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = get_min_max([3, 1, 4, 1, 5])
print(lo, hi)                        # 1 5

# 返回多个值也可以用 _ 忽略
_, hi2 = get_min_max([1, 2, 3])

# 返回复杂结构
def analyze(text):
    return {
        "length": len(text),
        "words": len(text.split()),
        "chars": list(text),
    }

print(analyze("hello world"))

# ---------- 3. 函数也是对象 ----------
# Python 中函数是一等公民，可以赋值给变量、作为参数传递、作为返回值
# Go 中函数也是一等类型，这点类似

def hello():
    return "hello"

f = hello                            # 赋值（不加括号！加括号是调用）
print(f())                           # hello

# 函数可以存到 list/dict 中
operations = {
    "greet": greet,
    "add": add,
}
print(operations["add"](1, 2))       # 3

# ---------- 4. 函数注解（类型提示）----------

def typed_add(a: int, b: int) -> int:
    return a + b

print(typed_add(1, 2))

# 参数注解：参数名: 类型
# 返回值注解：-> 类型
# 注解不影响运行，只是提示，后面类型注解章节详讲

def format_user(name: str, age: int = 18) -> str:
    return f"{name}({age})"

# ---------- 5. 函数的参数传递机制 ----------
# Python 参数传递是"传对象引用"（既不是纯值传递也不是纯引用传递）
#
# 不可变对象（int/str/tuple）：函数内修改相当于新建，不影响外部
# 可变对象（list/dict/set）：函数内修改会影响外部

def modify_immutable(x):
    x = x + 10                       # 新建对象，外部不变
    print("函数内:", x)

n = 5
modify_immutable(n)
print("函数外:", n)                  # 5

def modify_mutable(lst):
    lst.append(99)                   # 直接修改，外部也变
    print("函数内:", lst)

my_list = [1, 2]
modify_mutable(my_list)
print("函数外:", my_list)            # [1, 2, 99]

# 坑：如果不想让函数修改原 list，传入副本
# modify_mutable(my_list.copy())

# 这个机制和 Go 对比：
# Go 传 slice 时，底层数组是共享的（append 可能共享可能不共享）
# Python 传 list 始终共享同一个对象

def reassign(lst):
    lst = [9, 9, 9]                  # 重新赋值（让局部变量指向新对象），外部不变
    print("函数内:", lst)

my_list2 = [1, 2]
reassign(my_list2)
print("函数外:", my_list2)           # [1, 2]（重新赋值不影响外部）

# ---------- 6. 实战小例子 ----------

# 例子1：计算阶乘
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print(factorial(5))                  # 120

# 例子2：判断回文
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

print(is_palindrome("racecar"))      # True
print(is_palindrome("hello"))        # False

# 例子3：分页函数
def paginate(items, page=1, page_size=10):
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "data": items[start:end],
        "page": page,
        "total": len(items),
        "has_more": end < len(items),
    }

data = list(range(25))
print(paginate(data, page=2, page_size=10))
