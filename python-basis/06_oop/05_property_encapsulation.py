# ============================================================
# property 属性封装与访问控制
# ============================================================
# Go 中字段首字母大小写控制导出，getter/setter 是普通方法。
# Python 用 @property 可以把方法"伪装"成属性访问，
# 实现 getter/setter/校验，同时保持简洁的访问语法。
# ============================================================

# ---------- 1. property 基本用法（getter）----------

class Circle:
    def __init__(self, radius):
        self._radius = radius          # 下划线表示内部属性

    @property
    def radius(self):
        """读取半径，像属性一样访问，不用加括号"""
        return self._radius

    @property
    def area(self):
        """计算属性：面积，派生值不需要单独存储"""
        return 3.14159 * self._radius ** 2

    @property
    def circumference(self):
        return 2 * 3.14159 * self._radius

c = Circle(5)
print(c.radius)                        # 注意：没有括号，像访问属性
print(c.area)                          # 自动计算
print(c.circumference)
# c.radius = 10                       # 只定义 getter 时是只读的，报错

# 好处：外部代码简洁，内部可以随时改成计算逻辑而不影响调用方式

# ---------- 2. setter（校验和控制修改）----------

class Temperature:
    def __init__(self, celsius=0):
        self.celsius = celsius         # 走 setter 校验

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度 -273.15°C")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5 / 9   # 复用 celsius setter

t = Temperature(25)
print(t.celsius, t.fahrenheit)
t.celsius = 30                         # 走 setter
t.fahrenheit = 68
print(t.celsius)
# t.celsius = -300                    # 触发校验报错

# ---------- 3. deleter ----------

class User:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.deleter
    def name(self):
        print("删除名字")
        self._name = None

u = User("Tom")
del u.name
print(u.name)

# ---------- 4. 访问控制约定 ----------
# Python 没有真正的 private/protected，靠命名约定：

class AccessDemo:
    def __init__(self):
        self.public_attr = "公开"       # 任意访问
        self._protected = "受保护"      # 约定：外部不应该访问（单下划线）
        self.__private = "私有"        # 双下划线触发名称改写（name mangling）

    def get_private(self):
        return self.__private          # 类内部正常访问

a = AccessDemo()
print(a.public_attr)
print(a._protected)                    # 能访问，只是约定不要
# print(a.__private)                  # 外部直接访问报错！
print(a._AccessDemo__private)          # 实际被改名（不建议这么访问）
print(a.get_private())

# 双下划线不是为了安全，是为了避免子类命名冲突
# 实际开发中单下划线最常用，双下划线较少

# ---------- 5. property vs 直接属性 ----------
# Python 的哲学：先简单用公开属性，需要校验时再用 property 升级，
# 调用方式不变（不像 Java 一开始就写 getter/setter）。
# 这叫"统一访问原则"。

# ---------- 6. 实战小例子 ----------

# 例子1：用户模型（校验邮箱/年龄）
class UserProfile:
    def __init__(self, username, email, age):
        self.username = username
        self.email = email
        self.age = age

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value or "." not in value:
            raise ValueError(f"邮箱格式不合法: {value}")
        self._email = value.strip().lower()

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError("年龄必须是整数")
        if not (0 <= value <= 150):
            raise ValueError("年龄必须在0~150之间")
        self._age = value

    @property
    def display_name(self):
        return f"{self.username} <{self.email}>"

user = UserProfile("Tom", "A@B.COM ", 25)
print(user.display_name)

# 例子2：限速属性
class RateLimiter:
    def __init__(self, max_rps):
        self.max_rps = max_rps

    @property
    def max_rps(self):
        return self._max_rps

    @max_rps.setter
    def max_rps(self, value):
        if value <= 0:
            raise ValueError("速率必须为正")
        self._max_rps = int(value)
