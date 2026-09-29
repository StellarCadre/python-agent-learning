# ============================================================
# 类方法 @classmethod、静态方法 @staticmethod、实例方法
# ============================================================
# 三种方法的区别：
#   实例方法：第一个参数 self，可以访问实例属性
#   类方法：第一个参数 cls，可以访问类属性，常用于"工厂方法"
#   静态方法：没有 self/cls，和普通函数一样，只是放在类的命名空间里
#
# Go 没有这些区分，方法都属于类型。
# ============================================================

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # 实例方法：最常见，操作实例
    def format(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

    # 类方法：操作类，cls 是类本身
    @classmethod
    def from_string(cls, date_str):
        """从字符串创建 Date（工厂方法，类方法最典型的用途）"""
        year, month, day = map(int, date_str.split("-"))
        return cls(year, month, day)        # cls() 就是创建实例

    @classmethod
    def today(cls):
        import datetime
        t = datetime.date.today()
        return cls(t.year, t.month, t.day)

    # 静态方法：不需要 self 也不需要 cls，和类有关但不依赖类/实例数据
    @staticmethod
    def is_valid_date(year, month, day):
        """判断日期是否合法（逻辑上属于 Date，但不需要访问数据）"""
        if not (1 <= month <= 12):
            return False
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # 闰年2月29天
        if month == 2 and (year % 4 == 0 and year % 100 != 0 or year % 400 == 0):
            return day <= 29
        return 1 <= day <= days_in_month[month - 1]

# 实例方法通过实例调用
d = Date(2026, 9, 28)
print(d.format())

# 类方法通过类调用（不需要先有实例）
d2 = Date.from_string("2026-01-15")
print(d2.format())
print(Date.today().format())

# 静态方法通过类直接调用
print(Date.is_valid_date(2024, 2, 29))    # True
print(Date.is_valid_date(2026, 2, 29))    # False

# 三种方法都可以通过实例调用，但类方法/静态方法推荐通过类调用

# ---------- 对比总结 ----------
#
#             第一个参数    能访问实例    能访问类    典型用途
# 实例方法     self          是            是          操作实例数据
# 类方法       cls           否            是          工厂方法、操作类属性
# 静态方法     无            否            否          工具函数（和类相关）
#
# 什么时候用静态方法？
#   函数逻辑和类相关，但不需要读写类/实例数据，放类里更内聚。
#   如果完全无关，放模块级普通函数即可。

# ---------- 类方法工厂模式实战 ----------

class Config:
    def __init__(self, host, port, debug=False):
        self.host = host
        self.port = port
        self.debug = debug

    @classmethod
    def development(cls):
        return cls("localhost", 8000, debug=True)

    @classmethod
    def production(cls):
        return cls("0.0.0.0", 80, debug=False)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

dev = Config.development()
prod = Config.production()
custom = Config.from_dict({"host": "10.0.0.1", "port": 9090})
print(dev.host, prod.port, custom.host)

# ---------- 静态方法实战：工具类 ----------

class StringUtils:
    @staticmethod
    def reverse(s):
        return s[::-1]

    @staticmethod
    def count_words(s):
        return len(s.split())

    @staticmethod
    def truncate(s, max_len, suffix="..."):
        if len(s) <= max_len:
            return s
        return s[:max_len] + suffix

print(StringUtils.reverse("hello"))
print(StringUtils.truncate("这是一段很长的文本内容", 8))
