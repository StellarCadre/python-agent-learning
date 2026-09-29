# ============================================================
# 抽象基类（Abstract Base Class, ABC）
# ============================================================
# Go 的接口是隐式实现（鸭子类型，不需要声明 implements）：
#   type Tool interface { Run() string }
#
# Python 用 abc 模块定义抽象基类，可以强制子类实现某些方法，
# 否则子类无法实例化。Agent 框架中定义基类接口很常见。
# ============================================================

from abc import ABC, abstractmethod

# ---------- 1. 基本抽象类 ----------

class BaseAgent(ABC):
    """Agent 基类，子类必须实现 chat 方法"""

    def __init__(self, name):
        self.name = name

    @abstractmethod                  # 抽象方法：子类必须实现
    def chat(self, message: str) -> str:
        """处理用户消息"""
        ...

    # 普通方法：子类直接继承
    def intro(self):
        return f"我是 {self.name}"

# base = BaseAgent("test")           # 报错！抽象类不能实例化

class EchoAgent(BaseAgent):
    def chat(self, message):
        return f"回声：{message}"

echo = EchoAgent("回声机器人")
print(echo.intro())
print(echo.chat("你好"))

# 如果子类没实现全部抽象方法，仍然是抽象类，不能实例化
# class BadAgent(BaseAgent): pass
# BadAgent("x")                      # 报错

# ---------- 2. 抽象属性 ----------

class BaseModel(ABC):
    @property
    @abstractmethod
    def model_name(self):
        """子类必须提供 model_name 属性"""
        ...

    @abstractmethod
    def invoke(self, prompt):
        ...

class GPTModel(BaseModel):
    @property
    def model_name(self):
        return "gpt-4"

    def invoke(self, prompt):
        return f"[{self.model_name}] {prompt}"

m = GPTModel()
print(m.invoke("hello"))

# ---------- 3. 模板方法模式（抽象类的经典用法）----------

class DataProcessor(ABC):
    """数据处理模板：流程固定，具体步骤子类实现"""

    # 模板方法：定义处理流程（不重写）
    def process(self, raw_data):
        data = self.validate(raw_data)
        data = self.transform(data)
        result = self.save(data)
        return result

    @abstractmethod
    def validate(self, data):
        ...

    @abstractmethod
    def transform(self, data):
        ...

    # 钩子方法：子类可选重写（给默认实现）
    def save(self, data):
        return f"已保存 {data}"

class JSONProcessor(DataProcessor):
    def validate(self, data):
        print("校验 JSON")
        return data

    def transform(self, data):
        print("转换 JSON")
        return data.upper()

p = JSONProcessor()
print(p.process("hello"))

# ---------- 4. 鸭子类型 vs 抽象基类 ----------
# Python 崇尚鸭子类型："走起来像鸭子、叫起来像鸭子，就是鸭子"
# 不强制继承，只要有对应方法即可

class Duck:
    def quack(self):
        return "嘎嘎"

class Person:                         # 没有继承任何类
    def quack(self):
        return "人模仿嘎嘎"

def make_quack(obj):
    # 不检查类型，只要有 quack 方法就行
    print(obj.quack())

make_quack(Duck())
make_quack(Person())

# Go 的接口也是这个理念（结构化类型）
# 抽象基类适合需要"强制契约"的场景，普通鸭子类型更灵活

# 用 isinstance 检查是否实现了接口
from collections.abc import Iterable, Callable, Mapping

print(isinstance([1, 2], Iterable))   # True
print(isinstance("s", Iterable))
print(callable(print))                # True

# collections.abc 提供了很多抽象容器类型（了解）
# ---------- 5. 实战：Agent 工具接口 ----------

class Tool(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, **kwargs):
        ...

    # 通用方法
    def describe(self):
        return f"{self.name}: {self.description}"

class SearchTool(Tool):
    def __init__(self):
        super().__init__("search", "搜索网页")

    def run(self, query="", **kwargs):
        return f"搜索结果: {query}"

class WeatherTool(Tool):
    def __init__(self):
        super().__init__("weather", "查询天气")

    def run(self, city="", **kwargs):
        return f"{city}的天气: 晴"

tools = [SearchTool(), WeatherTool()]
for tool in tools:
    print(tool.describe(), "->", tool.run(query="python") if tool.name == "search" else tool.run(city="北京"))
