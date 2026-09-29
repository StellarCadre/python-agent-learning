# ============================================================
# 类（class）基础
# ============================================================
# Go 没有传统的类，用 struct + 方法接收者模拟：
#   type User struct { Name string; Age int }
#   func (u User) SayHi() string { return u.Name }
#
# Python 用 class 定义类，self 相当于 Go 的方法接收者。
# Agent 框架（LangChain、Pydantic）大量使用类，必须掌握。
# ============================================================

# ---------- 1. 定义最简单的类 ----------

class Dog:
    # __init__ 是初始化方法（构造方法），创建实例时自动调用
    # self 代表正在创建的实例本身，必须是第一个参数（调用时不用传）
    def __init__(self, name, age):
        # self.xxx 是实例属性（相当于 struct 字段）
        self.name = name
        self.age = age

    # 实例方法：第一个参数永远是 self
    def bark(self):
        return f"{self.name}：汪汪！"

    def describe(self):
        return f"{self.name}，{self.age}岁"

# 创建实例：类名(参数)，不需要 new（Go: &Dog{...}）
d1 = Dog("旺财", 3)
d2 = Dog("来福", 5)

# 访问属性
print(d1.name, d1.age)
# 调用方法
print(d1.bark())
print(d2.describe())

# 每个实例是独立对象，属性互不影响
d1.name = "小黑"
print(d1.name, d2.name)             # 小黑 来福

# ---------- 2. 属性可以动态添加（Python 特色，Go 不行）----------

d1.color = "黑色"                    # 只给 d1 加属性
print(d1.color)
# print(d2.color)                   # d2 没有，报错

# 不建议随意动态加属性，应该在 __init__ 里定义清楚

# ---------- 3. 类属性 vs 实例属性 ----------

class Cat:
    # 类属性：直接写在类里，所有实例共享（类似 Go 的包级常量/变量）
    species = "猫科动物"
    count = 0

    def __init__(self, name):
        self.name = name             # 实例属性
        Cat.count += 1               # 通过类名修改类属性

c1 = Cat("咪咪")
c2 = Cat("花花")

print(c1.species, c2.species)       # 都能访问类属性
print(Cat.species)                  # 推荐通过类名访问
print(Cat.count)                    # 2（统计创建了多少实例）

# 坑：通过实例给类属性赋值，不会修改类属性，而是创建同名实例属性（遮蔽）
c1.species = "我变了"
print(c1.species)                   # 我变了（实例属性遮蔽了类属性）
print(c2.species)                   # 猫科动物（类属性没变）
print(Cat.species)

# 删除实例属性后又能看到类属性
del c1.species
print(c1.species)                   # 猫科动物

# ---------- 4. __str__ 和 __repr__（字符串表示）----------

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # __str__：面向用户的显示（print/str 时调用），类似 Go 的 String() 方法
    def __str__(self):
        return f"点({self.x}, {self.y})"

    # __repr__：面向开发者的表示（调试、REPL），应该尽量详细
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

p = Point(3, 4)
print(p)                             # 点(3, 4)，调用 __str__
print(str(p))
print(repr(p))                       # Point(x=3, y=4)
print(p.__repr__())

# 如果只定义 __repr__ 没定义 __str__，会用 __repr__ 兜底
# 建议至少定义 __repr__

# Go 对比：Go 实现 Stringer 接口的 String() 方法相当于 __str__

# ---------- 5. self 的理解 ----------

class Counter:
    def __init__(self, start=0):
        self.value = start

    def increment(self):
        self.value += 1
        return self.value

cnt = Counter(10)
# 这两种调用等价：
print(cnt.increment())              # 自动把 cnt 作为 self 传入
print(Counter.increment(cnt))       # 显式传 self（不常用）

# Go: func (c *Counter) Increment()，c 就是 self
# Python 的 self 必须显式写在参数里（Go 的接收者也要写，但调用时自动）

# ---------- 6. 方法链式调用 ----------

class StringBuilder:
    def __init__(self):
        self.parts = []

    def add(self, text):
        self.parts.append(text)
        return self                  # 返回 self 支持链式调用

    def build(self):
        return " ".join(self.parts)

result = StringBuilder().add("hello").add("world").add("python").build()
print(result)

# ---------- 7. 实战小例子 ----------

# 例子1：完整的银行账户类
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("存款金额必须为正")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("取款金额必须为正")
        if amount > self.balance:
            raise ValueError("余额不足")
        self.balance -= amount
        return self.balance

    def __str__(self):
        return f"{self.owner}的账户，余额{self.balance}"

acc = BankAccount("Tom", 100)
acc.deposit(50)
acc.withdraw(30)
print(acc)

# 例子2：简单的栈（Stack）
class Stack:
    def __init__(self):
        self._items = []             # 下划线开头约定为内部使用

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("空栈不能弹出")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("空栈")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"

s = Stack()
s.push(1)
s.push(2)
print(s.pop(), len(s))

# 例子3：矩形类
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def is_square(self):
        return self.width == self.height

r = Rectangle(3, 4)
print(r.area(), r.perimeter(), r.is_square())
