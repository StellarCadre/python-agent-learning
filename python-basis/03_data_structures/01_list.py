# ============================================================
# list（列表）全面讲解
# ============================================================
# list 是 Python 中最常用的数据结构，相当于 Go 的 slice。
# 特点：有序、可变、可以存放任意类型、允许重复元素。
# ============================================================

# ---------- 1. list 的多种创建方式 ----------

# 方式1：方括号直接创建（最常用）
nums = [1, 2, 3]
empty1 = []                          # 空列表
mixed = [1, "hello", True, 3.14, None]  # 可以放不同类型（Go slice 不行）
nested = [[1, 2], [3, 4]]            # 可以嵌套

# 方式2：list() 构造函数
chars = list("abc")                  # 字符串转列表 ['a', 'b', 'c']
empty2 = list()                      # 空列表
from_tuple = list((1, 2, 3))         # tuple 转 list

# 方式3：列表推导式（后面专门讲）
squares = [x * x for x in range(5)]

# 方式4：重复创建
zeros = [0] * 5                      # [0, 0, 0, 0, 0]
matrix_row = [0] * 3

print(nums, empty1, mixed, nested, chars, squares, zeros)

# ---------- 2. 访问元素 ----------

fruits = ["apple", "banana", "cherry", "date"]

# 正索引（从0开始，和 Go 一样）
print(fruits[0])                     # apple
print(fruits[2])                     # cherry

# 负索引（Python 特色，从后往前数，-1 是最后一个）
print(fruits[-1])                    # date
print(fruits[-2])                    # cherry

# 嵌套列表访问
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(matrix[1][2])                  # 6（第二行第三列）

# 坑：索引越界会报 IndexError（Go 也会 panic）
# print(fruits[10])      # IndexError
# print(fruits[-10])     # IndexError

# ---------- 3. 切片（slice）----------
# 语法：list[start:stop:step]，左闭右开（包含 start，不包含 stop）

nums2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(nums2[2:5])                    # [2, 3, 4]（索引2到4）
print(nums2[:4])                     # [0, 1, 2, 3]（从头开始，start省略=0）
print(nums2[6:])                     # [6, 7, 8, 9]（到末尾，stop省略=末尾）
print(nums2[-3:])                    # [7, 8, 9]（最后3个）
print(nums2[:])                      # [0,1,...,9]（复制整个列表，常用！）
print(nums2[::2])                    # [0, 2, 4, 6, 8]（步长2）
print(nums2[1::2])                   # [1, 3, 5, 7, 9]（奇数索引）
print(nums2[::-1])                   # [9,8,...,0]（反转列表）
print(nums2[8:2:-1])                 # [8,7,6,5,4,3]（反向切片）

# 坑：切片越界不会报错，自动截断（和 Go slice 不同，Go 会 panic）
print(nums2[5:100])                  # [5,6,7,8,9]，不报错

# 切片是浅拷贝，修改切片不影响原列表（顶层元素）
copy_nums = nums2[:]
copy_nums[0] = 999
print(nums2[0])                      # 0（原列表不变）

# ---------- 4. 修改元素 ----------

fruits2 = ["apple", "banana", "cherry"]
fruits2[0] = "apricot"               # 修改单个元素
print(fruits2)

# 切片批量修改
fruits2[1:3] = ["blueberry", "coconut"]
print(fruits2)

nums3 = [1, 2, 3, 4, 5]
nums3[1:4] = [20, 30]                # 替换的数量可以和原数量不同
print(nums3)                         # [1, 20, 30, 5]

# ---------- 5. 添加元素 ----------

lst = [1, 2, 3]

lst.append(4)                        # 末尾添加一个元素（最常用）
print(lst)                           # [1, 2, 3, 4]

lst.insert(1, 99)                    # 在索引1处插入，后面元素后移
print(lst)                           # [1, 99, 2, 3, 4]

lst.extend([5, 6, 7])                # 末尾批量添加多个（相当于 Go 的 append(slice, other...)）
print(lst)                           # [1, 99, 2, 3, 4, 5, 6, 7]

# + 拼接（会创建新列表，原列表不变）
a = [1, 2]
b = [3, 4]
c = a + b
print(c, a)                          # [1,2,3,4] [1,2]

# 坑：append 一个列表会把整个列表当成一个元素
a1 = [1, 2]
a1.append([3, 4])
print(a1)                            # [1, 2, [3, 4]]（嵌套了！）
# 想要合并多个元素用 extend

# ---------- 6. 删除元素 ----------

lst2 = ["a", "b", "c", "d", "e"]

# remove：按值删除第一个匹配项
lst2.remove("c")
print(lst2)                          # ['a', 'b', 'd', 'e']
# 坑：值不存在会报 ValueError
# lst2.remove("z")    # ValueError

# pop：按索引删除并返回被删元素（Go slice 没有内置）
val = lst2.pop(1)                    # 删除索引1
print("被删:", val, "剩余:", lst2)   # 被删: b 剩余: ['a', 'd', 'e']
last = lst2.pop()                    # 不传参数默认删最后一个
print(last, lst2)                    # e ['a', 'd']

# del：按索引或切片删除
lst3 = [1, 2, 3, 4, 5]
del lst3[0]
print(lst3)                          # [2, 3, 4, 5]
del lst3[1:3]
print(lst3)                          # [2, 5]

# clear：清空整个列表
lst3.clear()
print(lst3)                          # []

# ---------- 7. 查找与统计 ----------

lst4 = [10, 20, 30, 20, 40, 20]

print(lst4.index(20))                # 第一个20的索引 1
print(lst4.index(20, 2))             # 从索引2开始找 3
# print(lst4.index(99))             # 找不到报 ValueError

print(lst4.count(20))                # 统计出现次数 3
print(len(lst4))                     # 长度 6
print(20 in lst4)                    # True（是否包含）
print(99 not in lst4)                # True

# ---------- 8. 排序 ----------

nums5 = [3, 1, 4, 1, 5, 9, 2, 6]

# sort()：原地排序（修改原列表），返回 None
nums5.sort()
print(nums5)                         # [1, 1, 2, 3, 4, 5, 6, 9]

nums5.sort(reverse=True)             # 降序
print(nums5)                         # [9, 6, 5, 4, 3, 2, 1, 1]

# 自定义排序 key
words = ["banana", "fig", "apple", "cherry"]
words.sort(key=len)                  # 按字符串长度排序
print(words)                         # ['fig', 'apple', 'banana', 'cherry']

words.sort(key=lambda w: w[1])       # 按第二个字母排序
print(words)

# sorted()：返回新列表，原列表不变（Go sort.Slice 是原地）
original = [3, 1, 2]
sorted_list = sorted(original)
print(sorted_list, original)         # [1,2,3] [3,1,2]
print(sorted(original, reverse=True))  # 降序新列表

# reverse()：反转列表（原地）
nums6 = [1, 2, 3]
nums6.reverse()
print(nums6)                         # [3, 2, 1]

# reversed()：返回反转迭代器，不改原列表
print(list(reversed([1, 2, 3])))     # [3, 2, 1]

# ---------- 9. 复制列表 ----------

a = [1, 2, 3]

# 三种常见复制方式
b1 = a.copy()                        # copy() 方法
b2 = a[:]                            # 切片
b3 = list(a)                         # list() 构造

print(b1, b2, b3)
print(b1 is a)                       # False（是不同的列表对象）

# 坑：以上都是浅拷贝！嵌套列表修改会互相影响
nested1 = [[1, 2], [3, 4]]
shallow = nested1.copy()
shallow[0][0] = 999
print(nested1)                       # [[999, 2], [3, 4]]（原列表也变了！）

# 深拷贝需要 copy 模块
import copy
deep = copy.deepcopy(nested1)
deep[0][0] = 111
print(nested1)                       # [[999, 2], [3, 4]]（不受影响）

# ---------- 10. 其他常用操作 ----------

# 遍历（for 循环章节详讲）
for item in ["a", "b", "c"]:
    print(item)

# 带索引遍历
for i, v in enumerate(["a", "b"]):
    print(i, v)

# zip 同时遍历多个列表
names = ["Tom", "Bob"]
scores = [90, 85]
for n, s in zip(names, scores):
    print(n, s)

# 列表拼接成字符串
print(", ".join(["a", "b", "c"]))    # a, b, c

# any / all
print(any([False, True, False]))     # True（任一为真）
print(all([True, True, False]))      # False（全部为真才 True）
print(all([1, 2, 3]))                # True（非零为真）
