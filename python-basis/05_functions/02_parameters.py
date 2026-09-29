# ============================================================
# 函数参数详解（重点，Python 参数比 Go 灵活很多）
# ============================================================
# 参数类型：
#   1. 位置参数（最普通）
#   2. 默认参数
#   3. 关键字参数
#   4. *args 可变位置参数
#   5. **kwargs 可变关键字参数
#   6. 仅限关键字参数（* 后面的参数）
#   7. 仅限位置参数（/ 前面的参数，Python 3.8+）
# ============================================================

# ---------- 1. 位置参数 ----------

def subtract(a, b):
    return a - b

print(subtract(10, 3))               # 按位置顺序传，a=10, b=3
print(subtract(3, 10))               # -7，顺序很重要

# ---------- 2. 默认参数 ----------

def greet(name, greeting="你好"):
    return f"{greeting}，{name}"

print(greet("Tom"))                  # 默认 greeting
print(greet("Tom", "早上好"))
print(greet("Tom", greeting="晚上好"))

# 默认参数必须放在非默认参数后面
# def bad(a=1, b): ...              # 语法错误

# 坑：默认参数在函数定义时只计算一次！
# 不要用可变对象（list/dict）做默认值

def bad_append(item, lst=[]):        # 危险！默认 list 在多次调用间共享
    lst.append(item)
    return lst

print(bad_append(1))                 # [1]
print(bad_append(2))                 # [1, 2]（不是 [2]！上次的还在）

# 正确写法：用 None 做哨兵
def good_append(item, lst=None):
    if lst is None:
        lst = []                     # 每次调用新建
    lst.append(item)
    return lst

print(good_append(1))                # [1]
print(good_append(2))                # [2]

# ---------- 3. 关键字参数 ----------
# 调用时通过 参数名=值 传参，顺序可以打乱

def describe_pet(animal, name, age):
    return f"{animal}叫{name}，{age}岁"

print(describe_pet(name="旺财", age=3, animal="狗"))  # 顺序无关

# 位置参数和关键字参数混用（位置参数必须在前面）
print(describe_pet("猫", age=2, name="咪咪"))
# print(describe_pet(animal="猫", "咪咪", age=2))  # 错误，位置参数不能在关键字参数后

# ---------- 4. *args 可变位置参数 ----------
# *args 收集多余的位置参数，打包成 tuple
# 相当于 Go 的 ...int 可变参数

def sum_all(*numbers):
    print("收到:", numbers, type(numbers))
    total = 0
    for n in numbers:
        total += n
    return total

print(sum_all(1, 2, 3))              # 6
print(sum_all(1, 2, 3, 4, 5))        # 15
print(sum_all())                     # 0（空 tuple）

# *args 和普通参数混用
def multiply_all(multiplier, *nums):
    return [n * multiplier for n in nums]

print(multiply_all(10, 1, 2, 3))     # [10, 20, 30]

# 调用时用 * 解包 list/tuple 传参
def add_three(a, b, c):
    return a + b + c

values = [1, 2, 3]
print(add_three(*values))            # 等价 add_three(1,2,3)

# ---------- 5. **kwargs 可变关键字参数 ----------
# **kwargs 收集多余的关键字参数，打包成 dict

def print_info(**info):
    print("收到:", info, type(info))
    for key, value in info.items():
        print(f"  {key}: {value}")

print_info(name="Tom", age=18, city="北京")

# 常见用法：透传参数（Agent SDK 中很常见）
def create_chat(model, messages, **options):
    config = {"model": model, "messages": messages}
    config.update(options)           # temperature, max_tokens 等都进 options
    return config

print(create_chat("gpt-4", [], temperature=0.5, max_tokens=100))

# 调用时用 ** 解包 dict 传参
config = {"name": "Bob", "age": 20}
print_info(**config)                 # 等价 print_info(name="Bob", age=20)

# ---------- 6. 参数完整组合顺序 ----------
# 正确顺序：def func(位置参数, /, 普通参数, *args, 仅限关键字参数, **kwargs)

def full_example(a, b, c=0, *args, d, e=0, **kwargs):
    # a, b：位置参数
    # c：默认参数
    # args：多余位置参数
    # d：仅限关键字参数（*args 后面，必须通过关键字传）
    # e：带默认值的仅限关键字参数
    # kwargs：多余关键字参数
    print(f"a={a}, b={b}, c={c}")
    print(f"args={args}")
    print(f"d={d}, e={e}")
    print(f"kwargs={kwargs}")

full_example(1, 2, 3, 4, 5, d=6, x=7, y=8)

# ---------- 7. 仅限关键字参数（* 后面）----------
# 单独一个 * 表示后面的参数必须用关键字传

def create_user(name, *, age, email):
    # age 和 email 必须写参数名
    return f"{name},{age},{email}"

print(create_user("Tom", age=18, email="a@b.com"))
# create_user("Tom", 18, "a@b.com")  # 错误！age/email 必须关键字传

# 这种设计可以提高可读性，布尔参数尤其适合
def send_message(to, content, *, urgent=False, encrypt=True):
    pass

# ---------- 8. 仅限位置参数（/ 前面，Python 3.8+）----------
# / 前面的参数只能按位置传，不能用关键字

def divmod_example(a, b, /):
    return a // b, a % b

print(divmod_example(10, 3))
# divmod_example(a=10, b=3)         # 错误！

# 实际开发中较少自己写，了解即可（很多内置函数是这种）

# ---------- 9. 实战小例子 ----------

# 例子1：灵活的日志函数
def log(level, message, *args, **kwargs):
    prefix = kwargs.pop("prefix", "[LOG]")
    timestamp = kwargs.pop("timestamp", "")
    if args:
        message = message.format(*args)
    extra = " ".join(f"{k}={v}" for k, v in kwargs.items())
    print(f"{prefix} {timestamp} [{level}] {message} {extra}")

log("INFO", "用户{}登录", 1001, ip="127.0.0.1")

# 例子2：配置合并函数
def build_config(required, default=None, **overrides):
    config = {"timeout": 30, "retries": 3}
    if default:
        config.update(default)
    config.update(overrides)
    config["required"] = required
    return config

print(build_config("api_call", {"timeout": 60}, retries=5, verbose=True))

# 例子3：模拟 print 函数签名
def my_print(*values, sep=" ", end="\n", file=None):
    output = sep.join(str(v) for v in values)
    print(output, end=end)

my_print("a", "b", "c", sep="-", end="!\n")
