# ============================================================
# dict（字典）全面讲解
# ============================================================
# dict 相当于 Go 的 map，存储键值对（key-value）。
# 特点：可变、通过 key 查找（不是索引）、key 必须可哈希（不可变类型）。
# Python 3.7+ dict 保持插入顺序（Go map 是无序的）。
#
# Agent 开发中 dict 极其高频：JSON 数据、模型参数、配置、
# 工具调用参数等都是 dict。
# ============================================================

# ---------- 1. dict 的多种创建方式 ----------

# 方式1：花括号字面量（最常用）
d1 = {"name": "Tom", "age": 18}
empty1 = {}                          # 空字典

# 方式2：dict() 构造函数
d2 = dict(name="Bob", age=20)        # 关键字参数方式（key 不用加引号）
d3 = dict([("name", "Alice"), ("age", 22)])  # 键值对列表
d4 = dict({"a": 1, "b": 2})          # 从另一个 dict 创建
empty2 = dict()

# 方式3：dict.fromkeys() 从可迭代对象创建，所有 key 共用一个默认值
keys = ["name", "age", "email"]
d5 = dict.fromkeys(keys, None)       # {'name': None, 'age': None, 'email': None}
d6 = dict.fromkeys(["a", "b"], 0)    # {'a': 0, 'b': 0}

# 方式4：字典推导式（后面专门讲）
d7 = {x: x * x for x in range(3)}

print(d1, d2, d3, d5, d7)

# key 可以是 str、int、float、bool、tuple（不可变类型）
# key 不能是 list、dict、set（可变类型，不可哈希）
mixed_keys = {
    1: "整数key",
    "str": "字符串key",
    (1, 2): "tuple key",
}
print(mixed_keys)

# 坑：bool 是 int 子类，True 和 1 是同一个 key，False 和 0 是同一个 key
weird = {True: "a", 1: "b"}
print(weird)                         # {True: 'b'}（后者覆盖前者）

# ---------- 2. 访问值 ----------

user = {"name": "Tom", "age": 18, "city": "北京"}

# 方式1：方括号取值（key 不存在会报 KeyError）
print(user["name"])                  # Tom
# print(user["email"])              # KeyError: 'email'

# 方式2：get() 安全取值（推荐，key 不存在返回 None，不报错）
print(user.get("age"))               # 18
print(user.get("email"))             # None
print(user.get("email", "未填写"))    # 可以指定默认值

# 方式3：setdefault()：key 存在返回值；不存在则设置默认值并返回
d = {"a": 1}
print(d.setdefault("a", 100))        # 1（已存在，默认值不生效）
print(d.setdefault("b", 200))        # 200（不存在，设置进去）
print(d)                             # {'a': 1, 'b': 200}

# ---------- 3. 添加和修改 ----------

person = {"name": "Tom"}

# 方括号直接赋值：key 存在则修改，不存在则添加
person["age"] = 18                   # 添加
person["name"] = "Bob"               # 修改
print(person)

# update()：批量更新/合并
person.update({"age": 20, "city": "上海"})
print(person)

person.update(email="a@b.com", height=1.75)  # 关键字方式
print(person)

# 合并字典（Python 3.9+ 支持 | 运算符）
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
merged = d1 | d2                     # b 被后者覆盖
print(merged)                        # {'a': 1, 'b': 3, 'c': 4}

# ---------- 4. 删除 ----------

d = {"a": 1, "b": 2, "c": 3, "d": 4}

# del：按 key 删除
del d["a"]
print(d)                             # {'b': 2, 'c': 3, 'd': 4}
# del d["z"]                        # key 不存在报 KeyError

# pop()：删除并返回值
val = d.pop("b")
print("删除:", val, "剩余:", d)      # 删除: 2 剩余: {'c': 3, 'd': 4}
print(d.pop("z", "默认"))            # key 不存在返回默认值，不报错

# popitem()：删除并返回最后插入的键值对（Python 3.7+）
item = d.popitem()
print("删除:", item, "剩余:", d)

# clear()：清空
d.clear()
print(d)                             # {}

# ---------- 5. 遍历 dict（重点，多种方式）----------

user2 = {"name": "Tom", "age": 18, "city": "北京"}

# 遍历 key（默认遍历的就是 key）
for key in user2:
    print(key) #结果是这几个key名

for key in user2.keys():
    print(key) #结果是这几个key名

# 遍历 value
for value in user2.values():
    print(value) #结果是这几个key对应的value

# 同时遍历 key 和 value（最常用！）
for key, value in user2.items():
    print(f"{key} = {value}")

# keys()/values()/items() 返回的是视图对象，不是 list
# 需要 list 时显式转换
print(list(user2.keys()))            # ['name', 'age', 'city']
print(list(user2.values()))          # ['Tom', 18, '北京']
print(list(user2.items()))           # [('name', 'Tom'), ('age', 18), ('city', '北京')]


# ---------- 6. 判断和统计 ----------

d = {"a": 1, "b": 2}

print("a" in d)                      # True（判断 key 是否存在）
print("z" not in d)                  # True
# 坑：in 判断的是 key，不是 value！
print(1 in d)                        # False（1 是 value 不是 key）

print(len(d))                        # 2（键值对数量）

# ---------- 7. 复制 ----------

d1 = {"a": 1, "b": [1, 2]}

d2 = d1.copy()                       # 浅拷贝
d3 = dict(d1)                        # 也是浅拷贝

print(d2 is d1)                      # False

# 坑：和 list 一样，嵌套可变对象浅拷贝会互相影响
d2["b"].append(3)
print(d1["b"])                       # [1, 2, 3]

# 深拷贝用 copy.deepcopy()
import copy
d4 = copy.deepcopy(d1)
d4["b"].append(4)
print(d1["b"])                       # [1, 2, 3]（不受影响）


# ---------- 8. 实际应用小例子 ----------
print("-----------------实际应用小例子------------------------")
# 例子1：统计字符出现次数（Agent 处理文本时常用）
text = "hello python"
counter = {}
for ch in text:
    counter[ch] = counter.get(ch, 0) + 1  #
print(counter)

# 例子2：按条件过滤字典
scores = {"Tom": 85, "Bob": 59, "Alice": 92, "David": 45}
passed = {name_new: score_new for name, score in scores.items() if score >= 60} #先将scores中的内容解析到name和score上，然后再传给passed的name_new: score_new
print(passed)                        # {'Tom': 85, 'Alice': 92}

# 例子3：dict 和 JSON 天然对应（后面 JSON 章节详讲）
import json
api_response = '{"id": 1, "name": "Tom", "tags": ["a", "b"]}'
data = json.loads(api_response)      # JSON 字符串 -> dict
print(data["tags"])                  # ['a', 'b']

# 例子4：合并配置（默认配置 + 用户配置覆盖）
default_config = {"model": "gpt-4", "temperature": 0.7, "max_tokens": 1000}
user_config = {"temperature": 0.2}
final_config = {**default_config, **user_config}   # 解包合并
print(final_config)                  # temperature 被覆盖为 0.2
