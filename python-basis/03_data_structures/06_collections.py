# ============================================================
# collections 模块常用工具
# ============================================================
# collections 是 Python 标准库，提供了比内置类型更强大的容器：
#   - Counter：计数器（统计频率极方便）
#   - defaultdict：带默认值的 dict
#   - OrderedDict：有序字典（Python 3.7+ 普通 dict 也有序，少用）
#   - namedtuple：命名元组（tuple 章节讲过）
#   - deque：双端队列
#   - ChainMap：链式映射
# Agent 开发中 Counter 和 defaultdict 比较常用。
# ============================================================

from collections import Counter, defaultdict, OrderedDict, deque, ChainMap

# ---------- 1. Counter 计数器 ----------
# Counter 是 dict 的子类，专门用来统计可哈希对象的出现次数

# 创建方式
c1 = Counter("hello world")          # 统计字符串中每个字符
print(c1)                            # Counter({'l': 3, 'o': 2, ...})

c2 = Counter(["apple", "banana", "apple", "cherry", "banana", "apple"])
print(c2)                            # Counter({'apple': 3, 'banana': 2, 'cherry': 1})

c3 = Counter(cat=3, dog=5, bird=2)   # 关键字方式
print(c3)

c4 = Counter({"red": 5, "blue": 3})
print(c4)

# 常用方法

# most_common：返回出现次数最多的 N 个元素
print(c1.most_common(3))             # 前3高频字符
print(c2.most_common(1))             # [('apple', 3)]

# elements：返回所有元素（按计数重复）
print(sorted(c3.elements()))         # ['bird','bird','cat','cat','cat','dog',...]

# total：总计数（Python 3.10+）
print(c3.total())                    # 10

# 访问计数（不存在返回 0，不报错，比普通 dict 方便）
print(c2["apple"])                   # 3
print(c2["grape"])                   # 0（普通 dict 会 KeyError）

# update：增加计数
c = Counter(a=1, b=2)
c.update({"a": 5, "c": 3})
print(c)                             # Counter({'a': 6, 'b': 2, 'c': 3})

# subtract：减少计数
c.subtract({"a": 2, "b": 10})
print(c)                             # a=4, b=-8（可以出现负数！）

# Counter 之间的运算
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2, c=1)
print(c1 + c2)                       # 相加（只保留正数）
print(c1 - c2)                       # 相减（只保留正数结果）
print(c1 & c2)                       # 交集取 min
print(c1 | c2)                       # 并集取 max

# 实战：词频统计
text = "python is great and python is easy to learn python"
word_counts = Counter(text.split())
print(word_counts.most_common(2))    # [('python', 3), ('is', 2)]

# ---------- 2. defaultdict 带默认值的字典 ----------
# 普通 dict 访问不存在的 key 报 KeyError，
# defaultdict 会自动用工厂函数生成默认值

# defaultdict(list)：不存在的 key 默认是空列表
dd1 = defaultdict(list)
dd1["fruits"].append("apple")        # key 不存在自动创建空 list 再 append
dd1["fruits"].append("banana")
dd1["veggies"].append("carrot")
print(dict(dd1))                     # {'fruits': ['apple','banana'], 'veggies': ['carrot']}

# 用普通 dict 写同样逻辑需要 setdefault，更啰嗦
d = {}
d.setdefault("fruits", []).append("apple")

# defaultdict(int)：默认是 0（计数场景）
dd2 = defaultdict(int)
for ch in "hello":
    dd2[ch] += 1                     # 不存在默认0，直接 += 1
print(dict(dd2))

# defaultdict(set)：默认是空集合
dd3 = defaultdict(set)
dd3["colors"].add("red")
dd3["colors"].add("blue")
dd3["colors"].add("red")             # 自动去重
print(dict(dd3))

# 自定义默认值函数
def default_value():
    return "未知"

dd4 = defaultdict(default_value)
print(dd4["name"])                   # 未知

# 坑：defaultdict 只有用 [] 访问才会生成默认值，get() 不会
print(dd4.get("age"))                # None（get 不触发默认工厂）

# 实战：数据分组
records = [
    ("北京", "张三"),
    ("上海", "李四"),
    ("北京", "王五"),
    ("上海", "赵六"),
    ("广州", "钱七"),
]
groups = defaultdict(list)
for city, person in records:
    groups[city].append(person)
print(dict(groups))


# ---------- 3. OrderedDict 有序字典 ----------
# Python 3.7 之前普通 dict 无序，OrderedDict 保证插入顺序
# Python 3.7+ 普通 dict 也有序，OrderedDict 用得少了
# 但它有一些额外方法：move_to_end, popitem(last=...)

od = OrderedDict(a=1, b=2, c=3)
od.move_to_end("a")                  # 把 a 移到末尾
print(list(od.keys()))               # ['b', 'c', 'a']
od.move_to_end("c", last=False)      # 移到开头
print(list(od.keys()))               # ['c', 'b', 'a']

# ---------- 4. deque 双端队列 ----------
# deque（double-ended queue）支持两端高效增删，
# list 从头部插入/删除是 O(n)，deque 两端都是 O(1)
# 相当于 Go 的 container/list 或环形队列

dq = deque([1, 2, 3])

# 右端操作
dq.append(4)                         # 右端添加
dq.pop()                             # 右端弹出

# 左端操作
dq.appendleft(0)                     # 左端添加
dq.popleft()                         # 左端弹出

print(dq)

# 批量添加
dq.extend([4, 5])
dq.extendleft([-1, -2])              # 注意：按逆序加入左端
print(dq)

# 旋转
dq2 = deque([1, 2, 3, 4, 5])
dq2.rotate(2)                        # 右旋2步（末尾移到开头）
print(dq2)                           # deque([4, 5, 1, 2, 3])
dq2.rotate(-2)                       # 左旋
print(dq2)

# maxlen 固定长度队列（满了自动挤掉另一端，常用于滑动窗口）
history = deque(maxlen=3)
for i in range(5):
    history.append(i)
print(history)                       # deque([2, 3, 4], maxlen=3)，只保留最近3个

# ---------- 5. ChainMap 链式映射 ----------
# 把多个 dict 逻辑上合并成一个（不实际复制），查找时按顺序找

default_config = {"model": "gpt-4", "temperature": 0.7}
env_config = {"temperature": 0.2}
cli_config = {"verbose": True}

chain = ChainMap(cli_config, env_config, default_config)
# 查找顺序：cli_config -> env_config -> default_config
print(chain["model"])                # gpt-4（来自 default）
print(chain["temperature"])          # 0.2（env 覆盖 default）
print(chain["verbose"])              # True

# 新增/修改只影响第一个 dict
chain["new_key"] = "value"
print(cli_config)                    # 被加到第一个 dict
