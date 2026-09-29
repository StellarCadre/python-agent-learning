# ============================================================
# 函数作用域（Scope）与命名空间
# ============================================================
# Go 的作用域：包级变量、函数内局部变量，通过首字母大小写控制可见性。
# Python 的作用域遵循 LEGB 规则：
#   L - Local：函数内部
#   E - Enclosing：外层嵌套函数
#   G - Global：模块级（当前文件）
#   B - Built-in：内置（len, print 等）
# 查找变量时按 L -> E -> G -> B 顺序。
# ============================================================

# ---------- 1. 局部变量与全局变量 ----------

global_var = "我是全局变量"

def test_scope():
    local_var = "我是局部变量"
    print(global_var)                # 函数内可以读全局变量
    print(local_var)

test_scope()
# print(local_var)                  # 报错，局部变量外部访问不到

# ---------- 2. 修改全局变量需要 global ----------

counter = 0

def increment_wrong():
    # counter += 1                   # 报错！Python 把 counter 当局部变量
    pass

def increment():
    global counter                   # 声明 counter 用全局的
    counter += 1

increment()
increment()
print(counter)                       # 2

# 坑：只要函数内某处对变量赋值，Python 就把它当局部变量，
# 即使赋值前有读取也会报错 UnboundLocalError

name = "全局"
def confused():
    # print(name)                    # 报错！下面有赋值，name 被视为局部
    name = "局部"

# 最佳实践：少用 global，通过参数传入、return 返回（和 Go 一样）

# ---------- 3. 嵌套函数与 nonlocal ----------

def outer():
    outer_var = "外层函数变量"

    def inner():
        print(outer_var)             # 可以读外层函数变量（Enclosing）

    inner()

outer()

# 修改外层函数变量需要 nonlocal
def counter_maker():
    count = 0

    def increment():
        nonlocal count               # 声明用外层（非全局）的 count
        count += 1
        return count

    return increment

c = counter_maker()
print(c(), c(), c())                 # 1 2 3（闭包，count 被记住）

# global vs nonlocal：
#   global 指向模块级变量
#   nonlocal 指向最近一层嵌套函数的变量

# ---------- 4. 闭包（Closure）----------
# 内层函数记住外层函数的变量，即使外层函数已经执行结束

def make_multiplier(factor):
    def multiply(n):
        return n * factor            # factor 被闭包记住
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5), triple(5))          # 10 15

# 查看闭包记住的变量
print(double.__closure__[0].cell_contents)   # 2

# Go 也支持闭包（匿名函数捕获外部变量），概念一致

# 实战：配置工厂
def make_api_caller(base_url, api_key):
    def call(endpoint, **params):
        url = f"{base_url}/{endpoint}"
        return {"url": url, "key": api_key, "params": params}
    return call

openai_caller = make_api_caller("https://api.openai.com", "sk-xxx")
print(openai_caller("chat/completions", model="gpt-4"))

# ---------- 5. 内置作用域 ----------
# Python 自带的函数和异常名在 Built-in 作用域，最后才查找

# 坑：覆盖内置名后，在当前作用域就用不了原版
# list = [1,2,3]   # 覆盖后 list() 构造函数失效
# print(list(range(5)))   # TypeError

# 查看所有内置名
import builtins
# print(dir(builtins))

# ---------- 6. 实战小例子 ----------

# 例子1：带状态的函数（不用 class 的简单方案）
def make_bank_account(initial=0):
    balance = initial

    def deposit(amount):
        nonlocal balance
        balance += amount
        return balance

    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return "余额不足"
        balance -= amount
        return balance

    def get_balance():
        return balance

    return {"deposit": deposit, "withdraw": withdraw, "balance": get_balance}

account = make_bank_account(100)
print(account["deposit"](50))        # 150
print(account["withdraw"](30))       # 120
print(account["balance"]())          # 120

# 例子2：装饰器的雏形（后面装饰器章节展开）
def with_logging(func):
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}，参数: {args}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 返回: {result}")
        return result
    return wrapper

def add(a, b):
    return a + b

logged_add = with_logging(add)
logged_add(1, 2)

# 例子3：缓存函数（记忆化）
def memoize(func):
    cache = {}

    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]
    return wrapper

@memoize
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(50))                       # 很快（缓存生效）
