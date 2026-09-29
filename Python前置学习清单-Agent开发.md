# Python 前置学习清单（面向 Agent 开发 · Go 开发者视角）

> **学习定位**：你已经有扎实的 Go 基础（Gin/GORM/MySQL/Redis），不是编程小白。
> 学 Python 的唯一目标是：**能独立写出一个 FastAPI 的 Agent 服务**，调用大模型、做 RAG、工具调用。
> **原则：够用即可，对比 Go 快速迁移，边做边学，不追求成为 Python 专家。**

---

## 目录

1. [环境与工具](#一环境与工具)
2. [基础语法（对比 Go）](#二基础语法对比-go)
3. [核心数据结构](#三核心数据结构)
4. [控制流](#四控制流)
5. [函数](#五函数)
6. [面向对象（重点）](#六面向对象重点)
7. [模块、包与标准库](#七模块包与标准库)
8. [异常处理](#八异常处理)
9. [文件与常用操作](#九文件与常用操作)
10. [Agent 必备进阶语法](#十agent-必备进阶语法)
11. [FastAPI Web 框架（核心）](#十一fastapi-web-框架核心)
12. [HTTP 请求与第三方库](#十二http-请求与第三方库)
13. [工程化与项目结构](#十三工程化与项目结构)
14. [不需要深入的部分](#十四不需要深入的部分)
15. [学习顺序与时间建议](#十五学习顺序与时间建议)

---

## 一、环境与工具

| 要学的内容 | 说明 | Go 对应物 |
|---|---|---|
| **Python 版本** | 安装 Python 3.10+（建议 3.11/3.12），Agent 生态普遍要求 3.10+ | Go 版本 |
| **pip** | Python 官方包管理器，用来装第三方库 | `go get` |
| **venv 虚拟环境** | 给每个项目创建独立依赖环境，**必学，避免项目间依赖冲突** | Go module 的环境隔离理念 |
| **requirements.txt** | 列出项目依赖及版本 | `go.mod` |
| **pyproject.toml** | 新一代项目配置/依赖声明文件（现代项目用） | `go.mod` 升级版 |
| **uv / poetry（可选）** | 更快更现代的包管理工具，uv 速度极快，推荐了解 | — |
| **IDE** | VS Code（装 Python 插件）或 PyCharm（社区版免费） | VS Code / GoLand |
| **交互式运行** | 会用 `python 文件.py`、以及 REPL（命令行敲 `python` 进入交互模式） | `go run` |

### 必练命令

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境（Windows PowerShell）
.venv\Scripts\Activate.ps1
# 激活虚拟环境（Linux/Mac）
source .venv/bin/activate

# 安装依赖
pip install fastapi uvicorn httpx

# 导出依赖清单
pip freeze > requirements.txt

# 根据清单安装
pip install -r requirements.txt

# 运行程序
python main.py
```

> **坑提示**：Windows 上若 PowerShell 激活虚拟环境报"禁止运行脚本"，需执行
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`。

---

## 二、基础语法（对比 Go）

### 变量与类型

```python
# Python 是动态类型，变量无需声明类型（Go 是静态类型）
name = "Tom"          # 字符串 str
age = 18              # 整数 int
height = 1.75         # 浮点数 float
is_ok = True          # 布尔 bool（注意首字母大写：True / False / None）

# 类型注解（可选但 FastAPI 必备，后面重点讲）
name: str = "Tom"
age: int = 18
```

| Go | Python |
|---|---|
| `var x int = 1` | `x = 1` |
| `x := 1` | `x = 1` |
| 常量 `const` | 没有真正的常量，约定全大写 `MAX = 100` |
| `true / false / nil` | `True / False / None` |

### 字符串

```python
s = "hello"
s = 'hello'                      # 单双引号都行
multi = """多行
字符串"""                        # 三引号支持多行

# f-string 格式化（最常用，必学）
name = "Tom"
msg = f"你好，{name}，明年 {age + 1} 岁"

# 常用方法
s.upper(); s.lower(); s.strip()
s.split(","); ",".join(["a", "b"])
s.replace("a", "b"); len(s)
```

### 输入输出与注释

```python
# 这是单行注释
print("hello")                  # 输出，相当于 fmt.Println
name = input("请输入：")         # 读取输入（Web 项目几乎用不到）

"""
这是多行字符串，
常被当作多行注释/文档说明使用
"""
```

---

## 三、核心数据结构

> 这是 Python 最常用的部分，务必熟练，**对应 Go 的 array/slice/map**。

### 1. list（列表）≈ Go 的 slice

```python
nums = [1, 2, 3]
nums.append(4)          # 末尾添加
nums.insert(0, 0)       # 指定位置插入
nums.remove(2)          # 删除第一个值为2的元素
nums.pop()              # 弹出末尾元素
nums[0]                 # 取值（支持负索引：nums[-1] 是最后一个）
nums[1:3]               # 切片，取索引1到2（左闭右开）
len(nums)               # 长度
nums.sort()             # 排序
3 in nums               # 判断是否包含

# 列表推导式（Python 特色，高频）
squares = [x * x for x in range(5)]          # [0,1,4,9,16]
evens = [x for x in range(10) if x % 2 == 0]
```

### 2. tuple（元组）≈ 不可变的 list

```python
point = (3, 4)
x, y = point            # 解包，很常用
def 返回多个值时本质就是 tuple
```

### 3. dict（字典）≈ Go 的 map

```python
user = {"name": "Tom", "age": 18}
user["name"]                       # 取值
user["email"] = "a@b.com"          # 新增/修改
user.get("name")                   # 安全取值，不存在返回 None
user.get("x", "默认值")            # 可给默认值
user.keys(); user.values(); user.items()
del user["age"]
"name" in user

# 字典推导式
d = {x: x * x for x in range(3)}   # {0:0, 1:1, 2:4}

# 遍历（最常用）
for key, value in user.items():
    print(key, value)
```

### 4. set（集合）≈ 去重的无序集合

```python
s = {1, 2, 3}
s.add(4); s.remove(1)
a = {1, 2, 3}; b = {2, 3, 4}
a & b          # 交集 {2,3}
a | b          # 并集 {1,2,3,4}
a - b          # 差集 {1}
list(set([1, 1, 2]))     # 去重 -> [1,2]
```

### 速查表

| Python | Go 对应 | 是否可变 |
|---|---|---|
| `list` `[]` | slice | 可变 |
| `tuple` `()` | 不可变数组 | 不可变 |
| `dict` `{k:v}` | map | 可变 |
| `set` `{}` | map[T]struct{} | 可变 |

---

## 四、控制流

```python
# 条件判断（注意冒号和缩进，Python 靠缩进区分代码块，没有花括号）
age = 20
if age >= 18:
    print("成年")
elif age >= 12:
    print("青少年")
else:
    print("儿童")

# 逻辑运算：and / or / not（Go 是 && / || / !）
if age > 0 and age < 120:
    pass                          # pass 是空语句，占位用

# for 循环（Python 只有 for...in 和 while，没有 Go 的三段式 for）
for i in range(5):                # range(5) = 0,1,2,3,4
    print(i)

fruits = ["apple", "banana"]
for index, fruit in enumerate(fruits):   # enumerate 同时拿索引和值
    print(index, fruit)

for ch in "abc":                  # 直接遍历字符串/列表
    print(ch)

# while 循环
count = 0
while count < 3:
    count += 1

# break / continue 同 Go
for i in range(10):
    if i == 5:
        break
    if i % 2 == 0:
        continue

# match-case（Python 3.10+，类似 switch）
match status:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case _:
        print("其他")
```

> **重点习惯差异**：Python 用**缩进（4个空格）**代替 Go 的 `{ }`，用冒号 `:` 开启代码块。缩进错了直接报错。

---

## 五、函数

```python
# 基本定义
def add(a, b):
    return a + b

# 默认参数
def greet(name, greeting="你好"):
    return f"{greeting}，{name}"

greet("Tom")                  # 你好，Tom
greet("Tom", "早上好")

# 关键字参数（调用时通过参数名传参，顺序可乱）
greet(greeting="嗨", name="Tom")

# 可变参数
def func(*args, **kwargs):
    # args 是一个 tuple，收集多余的位置参数
    # kwargs 是一个 dict，收集多余的关键字参数
    print(args, kwargs)

func(1, 2, 3, name="Tom", age=18)
# args = (1,2,3)，kwargs = {"name":"Tom","age":18}

# 返回多个值（本质返回 tuple）
def get_user():
    return 1, "Tom"
id, name = get_user()

# lambda 匿名函数（简单场景用）
square = lambda x: x * x
nums = [(1, "b"), (2, "a")]
nums.sort(key=lambda x: x[1])      # 按元组第二个元素排序
```

### 作用域

- 函数内部可以读全局变量，但要**修改**全局变量需声明 `global`
- 实际开发中尽量通过参数传递和返回值，少用全局变量（和 Go 一样的好实践）

---

## 六、面向对象（重点）

> Agent 框架（LangChain、Pydantic、FastAPI）**大量使用类**，这部分必须理解，Go 没有传统的类，需要重点适应。

```python
# 定义类
class User:
    # 构造方法（创建对象时自动调用），self 代表实例本身，类似其他语言的 this
    def __init__(self, name, age):
        self.name = name          # 实例属性
        self.age = age

    # 实例方法，第一个参数永远是 self
    def say_hi(self):
        return f"我是 {self.name}"

    # __str__ 定义 print 对象时显示什么（魔术方法）
    def __str__(self):
        return f"User({self.name}, {self.age})"

# 创建实例（不需要 new）
u = User("Tom", 18)
print(u.say_hi())
print(u.name)

# 继承
class Admin(User):
    def __init__(self, name, age, level):
        super().__init__(name, age)     # 调用父类构造方法
        self.level = level

    # 方法重写
    def say_hi(self):
        return f"管理员 {self.name}"

a = Admin("Boss", 30, 9)
print(a.say_hi())
```

### 必须理解的概念

| 概念 | 说明 |
|---|---|
| `class` | 类，对象的模板（≈ Go 的 struct 定义 + 它的方法集合） |
| `__init__` | 构造/初始化方法，创建实例时自动执行 |
| `self` | 实例自身，写实例方法时第一个参数必须是它（调用时不用手动传） |
| 属性 | `self.xxx` 绑定的数据（≈ struct 字段） |
| 方法 | 类里定义的函数（≈ Go 给 struct 定义的方法） |
| 继承 | `class Admin(User)` 子类获得父类能力 |
| `super()` | 调用父类的方法 |
| **魔术方法（dunder methods）** | 双下划线包裹的特殊方法，如 `__init__`、`__str__`、`__len__`，框架靠它们实现魔法 |

> **Go 对比理解**：把 `class User` 想象成 `type User struct{...}`，`self` 想象成 Go 方法接收者 `func (u User) SayHi()`，就好理解了。

---

## 七、模块、包与标准库

```python
# 一个 .py 文件就是一个模块（module），一个含 __init__.py 的文件夹是包（package）

# 导入方式
import math
math.sqrt(16)

from datetime import datetime
datetime.now()

from typing import List, Dict, Optional     # Agent 开发高频

import json as js                # as 起别名
```

### Agent 开发常用标准库（不用专门背，知道干嘛的即可）

| 标准库 | 用途 |
|---|---|
| `json` | JSON 序列化/反序列化（**极高频**，相当于 Go 的 encoding/json） |
| `os` | 环境变量、文件路径、系统交互 |
| `sys` | 解释器相关、命令行参数 |
| `pathlib` / `os.path` | 路径处理（推荐 pathlib，更现代） |
| `datetime` | 日期时间处理 |
| `typing` | 类型注解（List/Dict/Optional/Any，**FastAPI 必备**） |
| `logging` | 日志 |
| `time` | 时间、sleep |
| `re` | 正则表达式 |
| `dataclasses` | 数据类（写数据结构很方便） |
| `abc` | 抽象基类/接口 |
| `asyncio` | 异步编程（后面讲） |
| `http` | 内置 HTTP（一般用第三方 httpx） |

---

## 八、异常处理

> Python 用异常处理错误，**和 Go 的"返回 error"哲学不同**，必须适应。Agent 调用网络/模型时大量用 try。

```python
try:
    num = int("abc")            # 这里会抛 ValueError
except ValueError:
    print("值错误")
except (TypeError, KeyError) as e:
    print("其他错误", e)
except Exception as e:
    print("兜底捕获所有异常", e)
else:
    print("没有异常时执行")
finally:
    print("无论是否异常都执行（常用于关闭资源）")

# 主动抛出异常
raise ValueError("参数不合法")

# 自定义异常
class MyError(Exception):
    pass
```

> **关键差异**：Go 习惯 `if err != nil` 显式返回；Python 是出错就 `raise` 异常，用 `try/except` 捕获。不捕获会导致程序崩溃。

---

## 九、文件与常用操作

```python
# with 语句会自动关闭文件（上下文管理器，强烈推荐）
with open("a.txt", "r", encoding="utf-8") as f:
    content = f.read()          # 读全部
    # lines = f.readlines()     # 按行读

with open("b.txt", "w", encoding="utf-8") as f:
    f.write("hello")

# JSON 处理（Agent 最常用，必练）
import json

data = {"name": "Tom", "age": 18}
text = json.dumps(data, ensure_ascii=False)    # dict -> JSON 字符串
obj = json.loads(text)                         # JSON 字符串 -> dict

# 读写 JSON 文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

> `ensure_ascii=False` 让中文正常显示，否则中文会被转义成 `\uXXXX`，这是高频坑。

---

## 十、Agent 必备进阶语法

> 这部分是**写 FastAPI / Agent 的硬门槛**，基础语法过完后重点学这里。

### 1. 类型注解（Type Hints）⭐ FastAPI/Pydantic 的灵魂

```python
name: str = "Tom"
age: int = 18
items: list[str] = ["a", "b"]
user: dict[str, int] = {"a": 1}

from typing import Optional, Union, Any

def find_user(uid: int) -> Optional[str]:     # 可能返回 str 或 None
    ...

def process(data: Union[int, str]) -> Any:    # int 或 str
    ...
```

| 注解 | 含义 |
|---|---|
| `int / str / bool / float` | 基本类型 |
| `list[str]` | 字符串列表 |
| `dict[str, Any]` | 键为 str、值任意的字典 |
| `Optional[X]` | X 或 None（等价 `X | None`） |
| `Union[A, B]` | A 或 B |
| `Any` | 任意类型 |

> 类型注解本身不强制运行，但 **FastAPI 靠它自动校验参数、生成文档、做序列化**，必须会写。

### 2. 装饰器（Decorator）⭐ 框架里到处是 `@xxx`

```python
# 装饰器 = 在不修改原函数的情况下，给函数增加功能
def log(func):
    def wrapper(*args, **kwargs):
        print("调用前")
        result = func(*args, **kwargs)
        print("调用后")
        return result
    return wrapper

@log                      # 等价于 say = log(say)
def say(name):
    print(f"hello {name}")

say("Tom")
```

> 现阶段**要求看懂 `@app.get("/")`、`@app.post`、`@tool` 这些装饰器在干嘛**（标记/注册一个函数），能自己写简单装饰器即可，不用钻很深。

### 3. 异步编程 async/await ⭐ 并发调用大模型必备

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)        # await 等待异步操作（如 HTTP 请求）
    return "数据"

async def main():
    # 并发执行多个任务（重要：同时调用多个模型/接口，省时间）
    results = await asyncio.gather(
        fetch_data(),
        fetch_data(),
    )
    print(results)

asyncio.run(main())
```

| Python | Go 对比 |
|---|---|
| `async def` 定义协程 | 类似可挂起的函数 |
| `await` 等待异步结果 | — |
| `asyncio.gather(...)` 并发 | 类似 `errgroup` / 多个 goroutine + WaitGroup |
| 事件循环 event loop | Go 的调度器由 runtime 自动管，Python 需事件循环驱动 |

> FastAPI 支持 `async def` 接口；调用大模型用异步客户端（httpx/官方 SDK 的 async 版本）可并发，**理解 async/await 即可**。

### 4. 上下文管理器（with）

前面文件操作的 `with` 就是，自动处理"打开/关闭、获取/释放"，保证资源正确释放。知道 `with X as y` 的用法即可。

### 5. 生成器（Generator，了解）

```python
def counter():
    for i in range(3):
        yield i          # yield 逐个产出，不一次性占内存
for n in counter():
    print(n)
```

> 知道 `yield` 是"惰性逐个产出"即可，流式处理时会遇到，不用深入。

---

## 十一、FastAPI Web 框架（核心）

> 这是你写 Agent 服务的最终载体，**Python 部分的学习终点就是会用 FastAPI 写接口**。它和 Gin 定位一致，你会上手很快。

### 安装

```bash
pip install fastapi uvicorn httpx
# uvicorn 是运行 FastAPI 的 ASGI 服务器（≈ 内嵌的 HTTP server）
```

### 最小完整示例

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 定义请求体结构（Pydantic 模型，自动校验，≈ Go 的 DTO + validator）
class UserCreate(BaseModel):
    name: str
    age: int

# 定义响应结构
class UserResp(BaseModel):
    id: int
    name: str
    age: int

# 路由（装饰器注册），≈ r.GET("/")
@app.get("/")
def index():
    return {"msg": "hello"}

# 路径参数
@app.get("/user/{uid}")
def get_user(uid: int):
    return {"id": uid}

# 查询参数（?name=xx）
@app.get("/search")
def search(keyword: str, page: int = 1):
    return {"keyword": keyword, "page": page}

# POST + 请求体自动校验
@app.post("/user", response_model=UserResp)
def create_user(req: UserCreate):
    return UserResp(id=1, name=req.name, age=req.age)
```

运行：

```bash
uvicorn main:app --reload
# main 是文件名 main.py，app 是 FastAPI 实例，--reload 改代码自动重启
# 默认地址 http://127.0.0.1:8000
# 自动生成交互式文档：http://127.0.0.1:8000/docs
```

### 必须掌握的 FastAPI 知识点

| 知识点 | 说明 | Gin 对应 |
|---|---|---|
| 路由 `@app.get/post` | 注册接口 | `r.GET/POST` |
| 路径参数 | `@app.get("/user/{uid}")` | `/user/:id` |
| 查询参数 | 函数参数自动从 `?key=value` 取 | `c.Query` |
| **Pydantic 请求体** | 用 BaseModel 定义结构，自动校验+报错 | `ShouldBind + validator` |
| `response_model` | 约束/过滤返回结构 | VO |
| 异步接口 | `async def` + `await` | — |
| **流式返回 SSE** | 打字机效果返回大模型输出（`StreamingResponse`） | `c.Stream` |
| 依赖注入 `Depends` | 复用公共逻辑（如鉴权、取 DB 连接） | 中间件 |
| 异常处理 | `HTTPException` + 全局异常处理 | 统一响应/中间件 |
| 中间件 | 跨域 CORS、日志等 | Gin 中间件 |
| 跨域 CORS | `CORSMiddleware`（前后端分离必备） | CORS 中间件 |

### Pydantic（FastAPI 的数据校验核心，必学）

```python
from pydantic import BaseModel, Field

class ChatReq(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="用户消息")
    temperature: float = Field(default=0.7, ge=0, le=2)
```

> Pydantic ≈ 你学过的 **DTO + validator + 序列化**三合一，会定义字段、默认值、校验规则（min/max/ge/le）即可。

---

## 十二、HTTP 请求与第三方库

> Agent 要调用大模型 API，本质就是发 HTTP 请求。

| 库 | 说明 |
|---|---|
| **httpx** | 现代 HTTP 客户端，**支持同步和异步**，推荐（异步 FastAPI 搭配） |
| requests | 最经典老牌 HTTP 库，同步，资料最多 |
| openai | 大模型官方 SDK（内部就是 HTTP），学 Agent 时直接用它 |

```python
import httpx

# 同步
resp = httpx.get("https://api.example.com/data")
data = resp.json()

# 异步（FastAPI 里用）
async with httpx.AsyncClient() as client:
    resp = await client.post("http://...", json={"key": "value"})
    result = resp.json()
```

---

## 十三、工程化与项目结构

### 推荐的 Agent 服务项目结构（分层，和你的 Go 习惯一致）

```
agent_service/
├── .venv/                  # 虚拟环境
├── requirements.txt        # 依赖清单
├── main.py                 # 入口，创建 FastAPI、注册路由
├── config.py               # 配置（API Key、模型名，读环境变量）
├── routers/                # 路由层（≈ handler）
│   └── chat.py
├── schemas/                # Pydantic 模型（≈ DTO/VO）
│   └── chat.py
├── services/               # 业务/Agent 逻辑（≈ service）
│   └── agent.py
├── tools/                  # 工具函数（Function Calling）
│   └── tools.py
└── rag/                    # RAG 相关（加载、切片、向量库）
    └── retriever.py
```

### 配置管理

- 用环境变量或 `.env` 文件存 API Key（**不要把密钥写死提交**），配合 `pydantic-settings` 读取
- 对应你 Go 项目里的 config 包

---

## 十四、不需要深入的部分

> 控制范围，以下内容**初学一律跳过**，用到再说：

- ❌ Python 高级元编程（元类 metaclass、复杂描述符）
- ❌ 多线程/多进程底层（GIL、线程池细节）——Agent 用 asyncio 即可
- ❌ 复杂设计模式、函数式编程库
- ❌ Django 全家桶（你只需要 FastAPI，别同时学两个 Web 框架）
- ❌ NumPy / Pandas / Matplotlib（数据分析方向才需要，Agent 业务开发用不到）
- ❌ 机器学习/深度学习、PyTorch/TensorFlow（调 API 不需要训练）
- ❌ 爬虫框架 Scrapy（除非项目要爬数据）
- ❌ Tkinter 等 GUI 库
- ❌ 纠结各种包管理器之争（会 venv + pip 就能开工，uv/poetry 后期再说）

---

## 十五、学习顺序与时间建议

> 总计约 **5~7 天**即可达到"能写 Agent 服务"的水平，不用学透，边做边查。

| 阶段 | 内容 | 建议时间 |
|---|---|---|
| 1 | 环境搭建：Python、venv、pip、IDE、跑通 hello world | 半天 |
| 2 | 基础语法 + 数据结构（list/dict/set/tuple、推导式） | 1 天 |
| 3 | 控制流 + 函数（默认参数、*args/**kwargs、lambda） | 半天 |
| 4 | 面向对象（class、self、init、继承、魔术方法） | 1 天 |
| 5 | 异常处理 + 文件 + JSON + 常用标准库 | 半天 |
| 6 | 进阶：类型注解、装饰器、async/await | 1 天 |
| 7 | **FastAPI + Pydantic：路由、请求体、SSE、CORS** | 1~2 天 |
| 8 | httpx 发 HTTP 请求，搭出项目骨架 | 半天 |

### 学习方法建议

1. **对比 Go 学**：每学一个概念，想一下它对应 Go 的什么，迁移最快。
2. **多敲少看**：Python 语法简单但"手感"和 Go 差异大（缩进、self、冒号），一定要亲手敲。
3. **终点明确**：所有学习都服务于"用 FastAPI 写一个能接收问题、调用大模型、流式返回的接口"，做到这个就可以正式进入 Agent 学习。
4. **不懂先记**：装饰器、魔术方法等抽象概念，第一遍看懂用法即可，框架用多了自然理解。

---

## 附：Go → Python 核心对照速查

| 概念 | Go | Python |
|---|---|---|
| 变量声明 | `x := 1` | `x = 1` / `x: int = 1` |
| 常量 | `const X = 1` | 约定全大写 |
| 空值 | `nil` | `None` |
| 布尔 | `true / false` | `True / False` |
| 逻辑与或非 | `&& / || / !` | `and / or / not` |
| 数组/切片 | `[]int` | `list` |
| 映射 | `map[string]int` | `dict` |
| 集合 | `map[T]struct{}` | `set` |
| 条件 | `if {} else {}` | `if : ... else: ...` |
| 循环 | `for i:=0; i<n; i++` | `for i in range(n):` |
| 函数 | `func f(a int) int` | `def f(a: int) -> int:` |
| 错误处理 | `if err != nil` | `try / except` |
| 类/结构体 | `type T struct{}` + 方法 | `class T:` |
| 方法接收者 | `func (t T) M()` | `def M(self):` |
| 依赖管理 | `go.mod` | `requirements.txt` / `pyproject.toml` |
| 包安装 | `go get` | `pip install` |
| 并发 | goroutine | `async/await` + asyncio |
| Web 框架 | Gin | FastAPI |
| 参数绑定校验 | ShouldBind + validator | Pydantic BaseModel |
| JSON 处理 | encoding/json | json / Pydantic |

---

> **一句话总结**：Python 语法本身 2~3 天就能过完，真正的重点是 **类型注解 + 面向对象 + async/await + FastAPI/Pydantic** 这四块，它们直接决定你能不能顺利写 Agent。其余全部"用到再查"。
