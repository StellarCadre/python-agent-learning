# ============================================================
# 类型转换
# ============================================================
# Go 的类型转换需要显式：int64(x), string(bytes)
# Python 也需要显式转换，用类型名当函数：int(x), str(x), float(x)
# ============================================================

# ---------- 1. 转整数 int() ----------

# 字符串 -> int
print(int("123"))                    # 123
print(int("-45"))                    # -45
print(int("  66  "))                 # 66（自动去除空白）

# 不同进制字符串转 int
print(int("FF", 16))                 # 255（16进制）
print(int("1010", 2))                # 10（2进制）
print(int("17", 8))                  # 15（8进制）

# float -> int（截断小数部分，不是四舍五入！）
print(int(3.99))                     # 3
print(int(-3.99))                    # -3
# 想要四舍五入用 round()，想要向下取整用 math.floor()

# bool -> int
print(int(True))                     # 1
print(int(False))                    # 0

# 坑：无法转换会抛异常 ValueError
# int("12.34")    # 报错！字符串有小数点不能直接转 int
# int("abc")      # 报错！
# int("")         # 报错！空字符串

# ---------- 2. 转浮点数 float() ----------

print(float("3.14"))                 # 3.14
print(float("3"))                    # 3.0
print(float("1e3"))                  # 1000.0
print(float(".5"))                   # 0.5
print(float(5))                      # 5.0
print(float(True))                   # 1.0
print(float("inf"))                  # 无穷大
print(float("nan"))                  # Not a Number

# float("abc")   # 报错 ValueError

# ---------- 3. 转字符串 str() ----------
# 这是最常用、最不容易出错的转换

print(str(123))                      # "123"
print(str(3.14))                     # "3.14"
print(str(True))                     # "True"
print(str(None))                     # "None"
print(str([1, 2, 3]))                # "[1, 2, 3]"
print(str({"a": 1}))                 # "{'a': 1}"

# repr() 和 str() 类似，但 repr 倾向于返回"给开发者看"的表示
print(str("hello"))                  # hello
print(repr("hello"))                 # 'hello'（带引号）

# ---------- 4. 转布尔 bool() ----------

print(bool(1))                       # True
print(bool(0))                       # False
print(bool(""))                      # False
print(bool("0"))                     # True（非空字符串就是真，即使内容是"0"！）
print(bool([]))                      # False
print(bool([0]))                     # True

# ---------- 5. 数字之间的转换注意事项 ----------

# int -> float
print(float(10))                     # 10.0

# float -> int 会丢失精度
pi = 3.14159
pi_int = int(pi)
print(pi_int)                        # 3

# 大数字字符串注意
# print(int("3.0"))   # 报错！要先 float 再 int
print(int(float("3.0")))             # 3


# ---------- 6. 容器类型之间的转换 ----------

# list / tuple / set 互转
lst = [1, 2, 2, 3]
print(tuple(lst))                    # (1, 2, 2, 3)
print(set(lst))                      # {1, 2, 3}（去重）
print(list((4, 5, 6)))               # [4, 5, 6]
print(list({1, 2, 3}))               # [1, 2, 3]（顺序不保证）

# dict 相关转换
# 两个元素的序列可以转 dict
pairs = [("name", "Tom"), ("age", 18)]
print(dict(pairs))                   # {'name': 'Tom', 'age': 18}

print(list({"a": 1, "b": 2}))        # ['a', 'b']（dict 直接转 list 只保留 key）
print(list({"a": 1, "b": 2}.items()))  # [('a', 1), ('b', 2)]

# ---------- 7. 字符串和 bytes 转换 ----------

# str -> bytes
b = "你好".encode("utf-8")
print(b)

# bytes -> str
s = b.decode("utf-8")
print(s)

# 也可以用 bytes() 和 str()
b2 = bytes("abc", encoding="utf-8")
print(b2)
s2 = str(b2, encoding="utf-8")
print(s2)

# ---------- 8. 安全转换的小技巧 ----------
# 实际开发中转换用户输入，最好用 try/except 包裹（后面异常章节详讲）

def safe_int(value, default=0):
    """安全转整数，失败返回默认值"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

print(safe_int("123"))               # 123
print(safe_int("abc"))               # 0
print(safe_int(None))                # 0
print(safe_int("xyz", -1))           # -1
