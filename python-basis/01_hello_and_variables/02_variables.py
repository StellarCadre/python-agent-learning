# ============================================================
# 变量与基础语法
# ============================================================
# Go 是静态类型语言，变量必须声明类型：
#   var name string = "Tom"
#   name := "Tom"
#
# Python 是动态类型语言，变量直接赋值即可，无需声明类型：
#   name = "Tom"
#
# 变量本质上是一个"名字标签"，贴在对象上，而不是一个固定类型的盒子。
# ============================================================

# ---------- 1. 变量的基本声明 ----------

# 最常见的写法：直接赋值
name = "Tom"
age = 18
height = 1.75
is_student = True

print(name, age, height, is_student)

# 同时给多个变量赋值（Python 特色，很常用）
a, b, c = 1, 2, 3
print(a, b, c)

# 链式赋值：多个变量指向同一个值
x = y = z = 0
print(x, y, z)

# 交换两个变量（Go 需要第三个变量临时交换，Python 一行搞定）
m, n = 1, 2
m, n = n, m
print("交换后:", m, n)               # 交换后: 2 1

# ---------- 2. 变量的类型 ----------

# Python 中一切皆对象，变量本身没有固定类型，类型属于对象
# 可以用 type() 查看变量当前指向对象的类型
print(type(name))                   # <class 'str'>
print(type(age))                    # <class 'int'>
print(type(height))                 # <class 'float'>
print(type(is_student))             # <class 'bool'>

# 同一个变量可以被重新赋值为不同类型（Go 不允许，Python 允许）
value = 100
print(value, type(value))           # 100 <class 'int'>
value = "hello"
print(value, type(value))           # hello <class 'str'>
# 坑提示：虽然可以这么做，但实际开发中不建议频繁改变变量类型，
# 容易让代码难以维护，类型注解可以帮助避免这个问题。

# ---------- 3. 类型注解（Type Hint）----------
# 在变量名后面加 : 类型，可以标注预期类型
# 注意：类型注解只是"提示"，运行时不会强制检查！

name_str: str = "Tom"
age_int: int = 18
price: float = 9.9
flag: bool = False

# 即使注解写了 int，仍然可以赋值字符串（运行时不报错）
# age_int = "字符串"   # 编辑器会警告，但运行不会崩
# 在 Agent/FastAPI 项目中强烈建议写类型注解，后面有专门章节讲解。

# ---------- 4. 常量 ----------
# Python 没有真正的常量（Go 有 const），约定全大写命名表示"不应该修改"

MAX_CONNECTIONS = 100
PI = 3.14159
API_KEY = "sk-xxxx"

# 实际上还是可以改的，全大写只是君子约定：
# MAX_CONNECTIONS = 200   # 语法上允许，但不应该这么做

# ---------- 5. 命名规范 ----------
# Python 官方推荐蛇形命名（snake_case），Go 也推荐驼峰但风格不同：
#   Go:   userName, userAge
#   Python: user_name, user_age

first_name = "张"
last_name = "三"
user_age = 25

# 类名用大驼峰（PascalCase）：class UserService: ...
# 常量全大写：MAX_SIZE = 100
# 私有变量约定下划线开头：_internal_data（后面 OOP 章节讲）

# ---------- 6. Python 关键字（不能用作变量名）----------
# 常见关键字：
#   False, None, True, and, as, assert, async, await, break,
#   class, continue, def, del, elif, else, except, finally, for,
#   from, global, if, import, in, is, lambda, nonlocal, not, or,
#   pass, raise, return, try, while, with, yield, match, case
#
# 坑提示：不要用内置函数名做变量名！比如：
#   list = [1,2,3]    # 这会覆盖内置的 list 类型，后面再用 list() 就报错
#   type = 1          # 会覆盖 type() 函数
#   str, dict, id, len, print, input, sum, max, min 等都不要用作变量名

# ---------- 7. 查看变量内存地址 ----------
# id() 返回对象的内存地址标识（类似 Go 中取指针地址，但不完全一样）
num1 = 10
num2 = 10
print("num1 的 id:", id(num1))
print("num2 的 id:", id(num2))
# Python 有小整数缓存机制（-5~256），num1 和 num2 可能指向同一个对象

# ---------- 8. 删除变量 ----------
temp = 999
del temp
# print(temp)   # 报错 NameError: name 'temp' is not defined
# Go 有 GC 自动回收，Python 也有 GC，del 只是移除变量名引用
