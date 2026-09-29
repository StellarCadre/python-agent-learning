# ============================================================
# 数字类型：int（整数）、float（浮点数）、complex（复数）
# ============================================================
# Go 的数字类型：int, int8, int16, int32, int64,
#               uint, uint8, ..., float32, float64, complex64, complex128
# Python 的数字类型：int, float, complex
#   - Python 的 int 没有大小限制（Go 的 int 取决于平台，int64 有上限）
#   - Python 的 float 相当于 Go 的 float64（双精度）
#   - 复数 Agent 开发基本用不到，简单了解即可
# ============================================================

# ---------- 1. 整数 int ----------

i1 = 100
i2 = -50
i3 = 0

print(i1, i2, i3)
print(type(i1))                     # <class 'int'>

# Python 的整数可以无限大（Go 中 int64 最大约 9.2 * 10^18）
big_num = 999999999999999999999999999999
print(big_num * big_num)            # 不会溢出，自动处理大数

# 不同进制的写法
binary = 0b1010                     # 二进制（Go 也是 0b 开头）
octal = 0o17                        # 八进制（Go 是 0 或 0o 开头）
hexadecimal = 0xFF                  # 十六进制（Go 也是 0x 开头）
print(binary, octal, hexadecimal)   # 10 15 255

# 数字中的下划线分隔（Python 3.6+，提高可读性，Go 也支持）
million = 1_000_000
phone = 138_0013_8000
print(million, phone)

# ---------- 2. 浮点数 float ----------

f1 = 3.14
f2 = -0.5
f3 = 1.0                           # 即使是 .0 也是 float 不是 int
f4 = 1e5                           # 科学计数法 = 100000.0
f5 = 1.5e-3                        # = 0.0015

print(f1, f2, f3, f4, f5)
print(type(f1))                     # <class 'float'>

# 坑：浮点数精度问题（Go 的 float64 也有同样问题）
print(0.1 + 0.2)                    # 0.30000000000000004，不是 0.3！
print(0.1 + 0.2 == 0.3)             # False

# 精确计算小数需要用 decimal 模块（金融场景）
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))   # 0.3

# ---------- 3. 复数 complex（了解即可）----------

c1 = 3 + 4j
c2 = complex(3, 4)
print(c1, c2)
print(c1.real, c1.imag)             # 实部 3.0，虚部 4.0

# ---------- 4. 算术运算符 ----------

a, b = 10, 3

print(a + b)                        # 加法 13
print(a - b)                        # 减法 7
print(a * b)                        # 乘法 30
print(a / b)                        # 除法 3.333...（注意：/ 结果永远是 float！）
print(a // b)                       # 整除（向下取整）3
print(a % b)                        # 取余 1
print(a ** b)                       # 幂运算 1000（Go 用 math.Pow）

# Go 中整数相除还是整数（10/3=3），Python 中 / 永远返回 float
# 想要整数结果必须用 //
print(10 / 2)                       # 5.0（float）
print(10 // 2)                      # 5（int）

# // 是"向下取整"，负数时要注意
print(-7 // 2)                      # -4（不是 -3！因为 -3.5 向下取整是 -4）

# ---------- 5. 复合赋值运算符 ----------

x = 10
x += 5                              # 等价 x = x + 5（Go 也有）
x -= 3
x *= 2
x /= 4                              # 注意：/= 后 x 变成 float
x //= 2
x %= 3
x **= 2
print("x =", x)

# Python 没有 x++ 或 x-- 自增自减运算符！（Go 有）
# 只能写 x += 1 或 x -= 1

# ---------- 6. 比较运算符 ----------

print(3 > 2)                        # True
print(3 < 2)                        # False
print(3 == 3)                       # True
print(3 != 4)                       # True
print(3 >= 3)                       # True
print(3 <= 2)                       # False

# 链式比较（Python 特色，Go 不支持）
age = 25
print(18 <= age <= 60)              # True，等价于 18 <= age and age <= 60
print(0 < age < 100)                # True

# ---------- 7. 数学函数 ----------

# 内置数学函数
print(abs(-10))                     # 绝对值 10
print(max(1, 5, 3))                 # 最大值 5
print(min(1, 5, 3))                 # 最小值 1
print(sum([1, 2, 3]))               # 求和 6
print(pow(2, 10))                   # 幂 1024
print(round(3.14159, 2))            # 四舍五入保留2位 3.14
print(round(2.5))                   # 2（坑：Python 用银行家舍入，.5 取偶数）
print(divmod(10, 3))                # 返回 (商, 余数) = (3, 1)

# math 模块（需要导入，类似 Go 的 math 包）
import math

print(math.floor(3.9))              # 向下取整 3
print(math.ceil(3.1))               # 向上取整 4
print(math.sqrt(16))                # 平方根 4.0
print(math.pi)                      # 圆周率
print(math.log(100, 10))     # 对数 2.0
print(math.sin(math.pi / 2))        # 三角函数 1.0
print(math.factorial(5))            # 阶乘 120
print(math.gcd(12, 18))             # 最大公约数 6
