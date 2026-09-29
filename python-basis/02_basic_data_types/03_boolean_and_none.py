# ============================================================
# 布尔类型 bool 与空值 None
# ============================================================

# ---------- 1. 布尔值 ----------
# Go:   true, false（小写）
# Python: True, False（首字母大写！）

t = True
f = False
print(t, f)
print(type(t))                       # <class 'bool'>

# bool 是 int 的子类，True 等价于 1，False 等价于 0
print(True + True)                   # 2
print(True * 10)                     # 10
print(int(True), int(False))         # 1 0

# ---------- 2. 比较运算产生布尔值 ----------

print(5 > 3)                         # True
print(5 == 3)                        # False
print(5 != 3)                        # True

# 逻辑运算符：and / or / not（Go 是 && / || / !）
print(True and False)                # False
print(True or False)                 # True
print(not True)                      # False

age = 25
print(age > 0 and age < 120)         # True
print(age < 18 or age > 60)          # False

# 短路规则（和 Go 一样）
# and：第一个为 False 就不看后面了
# or：第一个为 True 就不看后面了

# ---------- 3. 真值测试（重要！）----------
# Python 中任何值都可以放在 if 里判断"真"或"假"，
# 不需要像 Go 那样显式写 == true 或 != nil

# 以下值在布尔上下文中为 False（假值）：
#   - None
#   - False
#   - 数字 0（包括 0, 0.0, 0j）
#   - 空字符串 ""
#   - 空容器：[]（空list）、{}（空dict）、()（空tuple）、set()（空set）
#   - 其他：空 range、自定义对象的 __bool__ 返回 False 等
#
# 除了以上值，其他都为 True

# 用 bool() 可以显式转换查看
print(bool(0))                       # False
print(bool(1))                       # True
print(bool(""))                      # False
print(bool("hello"))                 # True
print(bool([]))                      # False
print(bool([0]))                     # True（列表非空就是真，即使里面是0）
print(bool(None))                    # False
print(bool(-1))                      # True（非零数字都是真，包括负数）

# Go 中 slice 判空要写 len(s) == 0，Python 直接 if s: 即可
items = []
if not items:                        # 空列表为假，not items 为真
    print("列表为空")

# ---------- 4. and/or 的返回值（Python 特色，容易踩坑）----------
# Go 的 && / || 返回 bool，Python 的 and/or 返回的是参与运算的原值！

# or：从左到右找第一个"真值"，找到就返回它；全假返回最后一个
print(0 or "" or None or "默认值")   # 默认值（前面都是假，返回最后一个）
print("a" or "b")                    # a（第一个就是真）

# and：从左到右找第一个"假值"，找到就返回它；全真返回最后一个
print("a" and "b" and "c")           # c（全是真，返回最后）
print("a" and 0 and "c")             # 0（找到假值）

# 常见用法：设置默认值
name = None
display_name = name or "匿名用户"
print(display_name)                  # 匿名用户

# ---------- 5. None（空值）----------
# Go 的空值：nil（只能用于指针、slice、map、channel、interface、函数）
# Python 的空值：None（表示"什么都没有"）

x = None
print(x)
print(type(x))                       # <class 'NoneType'>

# 判断 None 必须用 is None，不要用 == None（规范写法）
result = None
if result is None:
    print("结果为空")

if result is not None:
    print("结果不为空:", result)

# 为什么用 is 而不是 ==？
# is 比较的是内存地址（是否同一个对象），== 比较的是值
# None 在整个程序中是单例对象，用 is 更准确、更快
# 自定义类可以重载 == 运算符，但 is 无法重载

# 函数没有 return 时默认返回 None（后面函数章节会验证）

# ---------- 6. is 与 == 的区别（重要，容易混淆）----------

a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)                        # True（值相等）
print(a is b)                        # False（不是同一个对象，内存地址不同）

c = a
print(c is a)                        # True（c 和 a 指向同一个列表）

# 小整数和短字符串 Python 会缓存，可能出现 is 也为 True 的情况：
x1 = 100
x2 = 100
print(x1 is x2)                      # True（小整数缓存，不要依赖这个特性！）

# 判断值相等一律用 ==，判断是否为 None / True / False 用 is
