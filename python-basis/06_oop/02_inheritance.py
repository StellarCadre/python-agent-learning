# ============================================================
# 继承（Inheritance）
# ============================================================
# Go 没有继承，用结构体嵌入（embedding）组合实现复用：
#   type Animal struct{ Name string }
#   type Dog struct{ Animal }   // 嵌入
#
# Python 支持继承，子类获得父类的属性和方法，可以重写。
# Agent 框架中经常通过继承基类来开发自定义工具/模型。
# ============================================================

# ---------- 1. 单继承基础 ----------

class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self):
        return f"{self.name}在吃东西"

    def sleep(self):
        return f"{self.name}在睡觉"

    def describe(self):
        return f"{self.name}，{self.age}岁"

# Dog 继承 Animal：class 子类(父类)
class Dog(Animal):
    def __init__(self, name, age, breed):
        # 调用父类的 __init__，必须先调用，否则父类属性没初始化
        super().__init__(name, age)
        self.breed = breed           # 子类新增属性

    # 子类新增方法
    def bark(self):
        return f"{self.name}：汪汪！"

    # 方法重写（Override）
    def describe(self):
        # 可以复用父类方法再扩展
        base = super().describe()
        return f"{base}，品种{self.breed}"

d = Dog("旺财", 3, "金毛")
print(d.eat())                       # 继承来的方法
print(d.sleep())
print(d.bark())                      # 子类自己的方法
print(d.describe())                  # 重写后的方法

# super() 表示父类对象，Go 嵌入后可以通过 字段名.方法 调用
# Python 用 super().方法()

# ---------- 2. 方法重写规则 ----------

class Bird(Animal):
    def __init__(self, name, age, can_fly=True):
        super().__init__(name, age)
        self.can_fly = can_fly

    def sleep(self):                 # 完全重写，不调用 super
        return f"{self.name}单脚站着睡觉"

b = Bird("鹦鹉", 2)
print(b.sleep())                     # 调用子类版本

# ---------- 3. 多层继承 ----------

class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def info(self):
        return f"品牌{self.brand}"

class Car(Vehicle):
    def __init__(self, brand, seats):
        super().__init__(brand)
        self.seats = seats

class ElectricCar(Car):              # 继承链：ElectricCar -> Car -> Vehicle
    def __init__(self, brand, seats, battery):
        super().__init__(brand, seats)
        self.battery = battery

    def info(self):
        return f"{super().info()}，{self.seats}座，电池{self.battery}kWh"

tesla = ElectricCar("特斯拉", 5, 75)
print(tesla.info())

# ---------- 4. 多继承（Python 支持，但要谨慎）----------
# Go 只能嵌入多个结构体（类似多继承但不是）
# Python 可以继承多个父类

class Flyable:
    def fly(self):
        return "会飞"

class Swimmable:
    def swim(self):
        return "会游泳"

# 多继承：同时获得两个父类的方法
class Duck(Animal, Flyable, Swimmable):
    def __init__(self, name, age):
        super().__init__(name, age)

duck = Duck("唐老鸭", 2)
print(duck.fly(), duck.swim(), duck.eat())

# 方法解析顺序 MRO：多个父类有同名方法时按顺序找
# 查看查找顺序
print(Duck.__mro__)

# 坑：多继承容易导致复杂的菱形继承问题，实际开发优先用组合，
# Agent 框架中多继承较少，了解即可

# ---------- 5. 继承中的类型判断 ----------

print(isinstance(d, Dog))            # True
print(isinstance(d, Animal))         # True（子类实例也是父类类型）
print(issubclass(Dog, Animal))       # True
print(issubclass(Duck, Animal))

# Go 用类型断言，Python 用 isinstance
# 坑：type(d) == Animal 为 False，type 不考虑继承，isinstance 才考虑

# ---------- 6. 所有类的根：object ----------
# Python 3 中所有类默认继承 object（类似 Java）
# class Foo: 等价于 class Foo(object)

print(issubclass(Animal, object))   # True

# ---------- 7. 方法重写的特殊情况：扩展而非替换 ----------

class Logger:
    def log(self, msg):
        print(f"[日志] {msg}")

class TimestampLogger(Logger):
    def log(self, msg):
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        super().log(f"{ts} {msg}")   # 包装父类方法

class LevelLogger(Logger):
    def __init__(self, level="INFO"):
        self.level = level

    def log(self, msg):
        super().log(f"[{self.level}] {msg}")

TimestampLogger().log("测试")
LevelLogger("ERROR").log("出错了")

# ---------- 8. 实战小例子 ----------

# 例子1：员工薪资系统
class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def salary(self):
        return self.base_salary

    def describe(self):
        return f"{self.name}，薪资{self.salary()}"

class Manager(Employee):
    def __init__(self, name, base_salary, bonus):
        super().__init__(name, base_salary)
        self.bonus = bonus

    def salary(self):
        return self.base_salary + self.bonus

class Developer(Employee):
    def __init__(self, name, base_salary, overtime_hours, overtime_rate=100):
        super().__init__(name, base_salary)
        self.ot_hours = overtime_hours
        self.ot_rate = overtime_rate

    def salary(self):
        return self.base_salary + self.ot_hours * self.ot_rate

m = Manager("张总", 20000, 8000)
dev = Developer("李工", 15000, 20)
print(m.describe())
print(dev.describe())

# 例子2：Agent 工具基类（模拟框架设计，非常实用的模式）
class BaseTool:
    """所有工具的基类，子类实现 run"""
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def run(self, **kwargs):
        raise NotImplementedError("子类必须实现 run 方法")

    def __call__(self, **kwargs):     # 让对象可以像函数一样调用
        return self.run(**kwargs)

class CalculatorTool(BaseTool):
    def __init__(self):
        super().__init__("calculator", "数学计算")

    def run(self, expression=None, **kwargs):
        # 简单模拟
        return f"计算 {expression}"

calc = CalculatorTool()
print(calc.run(expression="1+1"))
print(calc(expression="2*3"))        # __call__ 生效
