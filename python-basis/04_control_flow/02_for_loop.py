# ============================================================
# for 循环
# ============================================================
# Go 的 for 有三种形式：
#   for i := 0; i < n; i++ { ... }       三段式
#   for index, value := range slice { }  range 遍历
#   for item := range channel { }
#
# Python 只有一种 for：for 变量 in 可迭代对象
# 没有三段式 for，想要数字索引用 range()
# ============================================================

# ---------- 1. range 数字循环 ----------
# range(start, stop, step) 生成整数序列，不包含 stop

# range(stop)：0 到 stop-1
for i in range(5):
    print(i, end=" ")                # 0 1 2 3 4
print()

# range(start, stop)
for i in range(2, 6):
    print(i, end=" ")                # 2 3 4 5
print()

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i, end=" ")                # 0 2 4 6 8
print()

# step 可以是负数
for i in range(10, 0, -2):
    print(i, end=" ")                # 10 8 6 4 2
print()

# range 不直接是 list，是可迭代对象，需要时转 list
print(list(range(5)))                # [0,1,2,3,4]

# ---------- 2. 遍历列表 ----------

fruits = ["apple", "banana", "cherry"]

# 直接遍历元素（最常用）
for fruit in fruits:
    print(fruit)

# 遍历字符串
for ch in "abc":
    print(ch)

# ---------- 3. enumerate 同时获取索引和值 ----------
# Go: for index, value := range fruits
# Python: for index, value in enumerate(fruits)

for index, fruit in enumerate(fruits):
    print(f"第{index}个: {fruit}")

# enumerate 可以指定起始索引（默认0）
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")           # 从1开始编号

# ---------- 4. 遍历 dict ----------

user = {"name": "Tom", "age": 18}

# 遍历 key
for key in user:
    print(key)

# 遍历 key 和 value
for key, value in user.items():
    print(f"{key}={value}")

# ---------- 5. 遍历多个序列 zip ----------
# Go 没有内置，需要手动按索引
# Python 用 zip 并行遍历，以最短的为准

names = ["Tom", "Bob", "Alice"]
scores = [90, 85, 95]

for name, score in zip(names, scores):
    print(f"{name}: {score}分")

# zip 长度不一致时以短的为准（多余的被忽略）
for a, b in zip([1, 2, 3], ["a", "b"]):
    print(a, b)                      # 只有2组

# 想以长的为准用 zip_longest
from itertools import zip_longest
for a, b in zip_longest([1, 2, 3], ["a"], fillvalue="默认"):
    print(a, b)

# ---------- 6. break 和 continue ----------

# break：立即跳出整个循环（Go 也有）
for i in range(10):
    if i == 5:
        print("找到5，结束")
        break
    print(i, end=" ")
print()

# continue：跳过本次，进入下一次
for i in range(6):
    if i % 2 == 0:
        continue
    print(i, end=" ")                # 1 3 5
print()

# 坑：Python 没有 do-while 循环

# ---------- 7. for...else（Python 特色，容易困惑）----------
# for 循环正常结束（没有被 break 中断）会执行 else 块
# 如果被 break 跳出，else 不执行
# 这个语法在"查找"场景很有用

# 找列表中第一个偶数
numbers = [1, 3, 5, 6, 7]
for n in numbers:
    if n % 2 == 0:
        print("找到偶数:", n)
        break
else:
    print("没有找到偶数")             # 被 break 了，不执行

# 全部是奇数时
for n in [1, 3, 5]:
    if n % 2 == 0:
        print("找到偶数")
        break
else:
    print("没有找到偶数")             # 正常结束，执行 else

# while 也有 else，同理
# 这个语法初看不习惯，理解为"循环没被 break 打断就执行"即可

# ---------- 8. 嵌套循环 ----------

# 乘法表
for i in range(1, 4):
    for j in range(1, i + 1):
        print(f"{j}x{i}={i*j}", end="\t")
    print()                          # 内层结束换行

# break 只跳出最内层循环
for i in range(3):
    for j in range(3):
        if j == 1:
            break                    # 只跳出 j 循环，i 继续
        print(i, j)

# ---------- 9. 实战小例子 ----------

# 例子1：冒泡排序（理解循环）
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:              # 一轮没交换说明已有序
            break
    return arr

print(bubble_sort([5, 2, 8, 1, 9]))

# 例子2：统计列表中各类元素
data = [1, "a", 2, "b", 3, "c"]
type_count = {}
for item in data:
    t = type(item).__name__
    type_count[t] = type_count.get(t, 0) + 1
print(type_count)                    # {'int': 3, 'str': 3}

# 例子3：查找两个列表的交集（不用 set）
a = [1, 2, 3, 4]
b = [3, 4, 5, 6]
common = []
for x in a:
    if x in b and x not in common:
        common.append(x)
print(common)
