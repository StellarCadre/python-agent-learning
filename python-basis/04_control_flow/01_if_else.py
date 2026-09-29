# ============================================================
# 条件判断 if / elif / else
# ============================================================
# Go 写法：
#   if age >= 18 {
#       ...
#   } else if age >= 12 {
#       ...
#   } else {
#       ...
#   }
#
# Python 写法：用冒号和缩进代替花括号，elif 是 else if 的缩写
#   if 条件:
#       ...
#   elif 条件:
#       ...
#   else:
#       ...
# ============================================================

# ---------- 1. 基本条件判断 ----------

age = 20

if age >= 18:
    print("成年")
elif age >= 12:
    print("青少年")
else:
    print("儿童")

# 注意：
# 1. 每个条件行末尾必须有冒号 :
# 2. 代码块靠缩进（通常4个空格）区分，没有花括号
# 3. Go 的 else if 在 Python 中写成 elif（一个词）
# 4. 缩进必须一致，混用空格和 Tab 会报错

# ---------- 2. 逻辑运算符组合条件 ----------

# Go: && || !
# Python: and or not
temperature = 25

if temperature > 0 and temperature < 35:
    print("温度适宜")

is_raining = False
if not is_raining:
    print("不下雨，可以出门")

# 优先级：not > and > or（建议用括号明确意图）
a, b, c = True, False, False
print(a or b and c)                 # True（先算 b and c=False，再 a or False）
print((a or b) and c)               # False

# ---------- 3. 成员判断作为条件 ----------

user_role = "admin"

if user_role in ["admin", "superadmin"]:
    print("有管理权限")

blocked_words = {"暴力", "违法"}
content = "今天天气不错"
if not any(w in content for w in blocked_words):
    print("内容正常")

# ---------- 4. 真值判断（Python 特色，前面讲过）----------
# 不需要显式比较，直接把值放 if 里

name = ""
if name:                             # 空字符串为假
    print("有名字")
else:
    print("名字为空")

items = [1, 2]
if items:                            # 非空列表为真
    print("列表有内容")

result = None
if result is None:                   # None 判断用 is None
    print("没有结果")

# Go 中要写 len(items) > 0、err != nil，Python 直接判断即可
# 但判断 True/False 时，PEP8 建议直接写 if flag: 而不是 if flag == True:

flag = True
if flag:                             # 推荐
    print("flag 为真")
# if flag == True:                  # 不推荐，多此一举

# ---------- 5. if 三元表达式 ----------
# Go 没有专门的三元运算符（Go 中只能写 if/else）
# Python 有：值A if 条件 else 值B

score = 85
result = "及格" if score >= 60 else "不及格"
print(result)                        # 及格

# 嵌套三元（不建议太深，可读性差）
grade = "优" if score >= 90 else ("良" if score >= 80 else "中")
print(grade)

# 变量赋值的常见用法
message = get_name() if has_name else "匿名" if False else "未知"

# ---------- 6. pass 空语句 ----------
# Python 要求缩进块里至少有一条语句，暂时不想写内容用 pass 占位
# Go 中可以写空 {}，Python 不能什么都不写

status = "pending"
if status == "done":
    pass                             # 后续实现，先占位
elif status == "pending":
    print("处理中")
else:
    pass

# 坑：pass 和 continue 不同，pass 是什么都不做然后继续往下执行，
# continue 是跳过本次循环进入下一次

# ---------- 7. 实战小例子 ----------

# 例子1：成绩等级判断
def get_grade(score):
    if score < 0 or score > 100:
        return "无效成绩"
    elif score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

print(get_grade(85))                 # B
print(get_grade(55))                 # F
print(get_grade(120))                # 无效成绩

# 例子2：简单的权限检查
def check_access(user, resource):
    if user is None:
        return "请先登录"
    if user.get("is_banned"):
        return "账号已封禁"
    if user.get("role") == "admin":
        return "允许访问所有资源"
    if resource in user.get("allowed", []):
        return "允许访问"
    return "无权限"

admin = {"role": "admin", "is_banned": False}
print(check_access(admin, "任何资源"))

# 例子3：判断闰年
def is_leap_year(year):
    # 能被4整除且不能被100整除，或者能被400整除
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False

print(is_leap_year(2024))            # True
print(is_leap_year(1900))            # False
print(is_leap_year(2000))            # True
