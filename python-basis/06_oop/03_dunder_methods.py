# ============================================================
# 魔术方法（Dunder Methods / Magic Methods）
# ============================================================
# 双下划线包裹的特殊方法（double underscore -> dunder），
# 如 __init__、__str__、__len__、__add__ 等。
# 它们不会被直接调用，而是在使用运算符或内置函数时自动触发。
# 框架靠这些方法实现"魔法"，Pydantic/LangChain 大量使用。
#
# Go 没有这种机制，最接近的是实现某些接口（如 Stringer）。
# ============================================================

# ---------- 1. 对象生命周期 ----------

class LifeCycle:
    def __new__(cls, *args, **kwargs):
        # __new__ 创建实例（在 __init__ 之前），很少自己写
        print("1. __new__ 创建对象")
        return super().__new__(cls)

    def __init__(self, value):
        print("2. __init__ 初始化")
        self.value = value

    def __del__(self):
        # 对象被垃圾回收时调用（时机不确定，不要依赖）
        print("3. __del__ 对象被回收")

obj = LifeCycle(42)
del obj

# ---------- 2. 比较运算符魔术方法 ----------

class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    # ==
    def __eq__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.celsius == other.celsius

    # <
    def __lt__(self, other):
        return self.celsius < other.celsius

    # <=
    def __le__(self, other):
        return self.celsius <= other.celsius

    # >
    def __gt__(self, other):
        return self.celsius > other.celsius

    def __str__(self):
        return f"{self.celsius}°C"

t1 = Temperature(25)
t2 = Temperature(30)
print(t1 == Temperature(25))         # True
print(t1 < t2)                       # True
print(t2 > t1)
# 定义 __eq__ 和 __lt__ 后，<= > >= 通常也能推断，建议都写

# 实现比较后可以直接 sorted
temps = [Temperature(30), Temperature(20), Temperature(25)]
print(sorted(temps))

# functools.total_ordering 可以只写 __eq__ 和一个比较就补全其他
from functools import total_ordering

# ---------- 3. 算术运算符 ----------

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):        # +
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):        # -
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):       # *（乘以数字）
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):   # /
        return Vector(self.x / scalar, self.y / scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __abs__(self):               # abs()
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)                       # Vector(4, 6)
print(v2 * 2)                        # Vector(6, 8)
print(abs(v2))                       # 5.0

# ---------- 4. 容器相关魔术方法 ----------

class MyList:
    def __init__(self, items=None):
        self._items = list(items or [])

    def __len__(self):               # len()
        return len(self._items)

    def __getitem__(self, index):    # obj[index]
        return self._items[index]

    def __setitem__(self, index, value):  # obj[index] = value
        self._items[index] = value

    def __delitem__(self, index):    # del obj[index]
        del self._items[index]

    def __contains__(self, item):    # item in obj
        return item in self._items

    def __iter__(self):              # for x in obj
        return iter(self._items)

    def __repr__(self):
        return f"MyList({self._items})"

ml = MyList([1, 2, 3])
print(len(ml))
print(ml[0])
ml[0] = 99
print(2 in ml)
for x in ml:
    print(x, end=" ")
print()

# ---------- 5. 对象转字符串/数字 ----------

class Money:
    def __init__(self, amount, currency="CNY"):
        self.amount = amount
        self.currency = currency

    def __str__(self):               # print/str
        return f"{self.amount:.2f} {self.currency}"

    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"

    def __int__(self):
        return int(self.amount)

    def __float__(self):
        return float(self.amount)

    def __bool__(self):              # bool()，非0为真
        return self.amount != 0

m = Money(99.5)
print(m, repr(m), int(m), bool(Money(0)))

# ---------- 6. __call__ 让对象像函数一样调用 ----------

class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        return value * self.factor

double = Multiplier(2)
print(double(21))                    # 42（对象当函数用）

# 常见用途：带状态的函数、API 客户端、装饰器类

# ---------- 7. 属性访问相关（了解）----------

class AttrDemo:
    def __init__(self):
        self.data = {}

    def __getattr__(self, name):
        # 访问不存在的属性时调用
        return self.data.get(name, f"属性{name}不存在")

    def __setattr__(self, name, value):
        # 设置任何属性时调用（容易递归，要小心）
        if name == "data":
            super().__setattr__(name, value)
        else:
            self.data[name] = value

ad = AttrDemo()
ad.x = 1
print(ad.x, ad.y)

# ---------- 8. with 上下文管理器魔术方法 ----------
# __enter__ 和 __exit__，后面上下文管理器章节详讲

# ---------- 9. 常用魔术方法速查表 ----------
#
# 类别        方法
# 初始化      __new__, __init__, __del__
# 字符串      __str__, __repr__, __format__
# 比较        __eq__, __ne__, __lt__, __le__, __gt__, __ge__
# 算术        __add__, __sub__, __mul__, __truediv__, __floordiv__,
#             __mod__, __pow__
# 容器        __len__, __getitem__, __setitem__, __delitem__,
#             __contains__, __iter__, __next__
# 转换        __int__, __float__, __bool__, __hash__
# 调用        __call__
# 属性        __getattr__, __setattr__, __delattr__, __getattribute__
# 上下文      __enter__, __exit__
#
# 建议：理解 __init__/__str__/__repr__/__eq__/__len__/__call__ 即可，
# 其他用到再查，不要死记。
