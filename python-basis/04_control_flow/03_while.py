# ============================================================
# while 循环
# ============================================================
# Go 的 while 写法：for 条件 { ... }
# Python 的 while：while 条件: ...
# Python 没有 do-while。
# ============================================================

# ---------- 1. 基本 while ----------

count = 0
while count < 5:
    print(count, end=" ")
    count += 1
print()

# 坑：Python 没有 count++，只能 count += 1
# 忘记修改条件变量会导致死循环

# ---------- 2. break / continue ----------

# break 跳出
i = 0
while True:                           # 无限循环（Go: for {}）
    if i >= 3:
        print("结束")
        break
    print(i, end=" ")
    i += 1
print()

# continue 跳过本次
i = 0
while i < 6:
    i += 1
    if i % 2 == 0:
        continue
    print(i, end=" ")                # 1 3 5
print()

# ---------- 3. while...else ----------
# 和 for...else 一样，没被 break 就执行 else

i = 0
while i < 3:
    print(i, end=" ")
    i += 1
else:
    print("正常结束")

# 被 break 时不执行 else
i = 0
while i < 5:
    if i == 2:
        print("被break")
        break
    i += 1
else:
    print("不会执行")

# ---------- 4. 实战小例子 ----------

# 例子1：猜数字游戏
def guess_game(target=42):
    attempts = 0
    while True:
        attempts += 1
        # 这里模拟猜测，实际可用 input()
        guess = target               # 直接猜中
        if guess == target:
            print(f"猜对了，用了{attempts}次")
            break
        elif guess < target:
            print("小了")
        else:
            print("大了")

guess_game()

# 例子2：逐位处理数字
n = 12345
digits = []
while n > 0:
    digits.append(n % 10)
    n //= 10
print(digits)                        # [5,4,3,2,1]（逆序）
print(digits[::-1])                  # [1,2,3,4,5]

# 例子3：轮询/重试机制（Agent 调用 API 常用）
import time

def retry_request(max_retries=3):
    """模拟带重试的请求"""
    attempt = 0
    while attempt < max_retries:
        attempt += 1
        success = attempt == 3       # 第3次成功
        if success:
            print(f"第{attempt}次请求成功")
            return True
        wait = 2 ** attempt          # 指数退避：2,4,8...
        print(f"第{attempt}次失败，等待{wait}秒")
        # time.sleep(wait)           # 实际等待
    print("重试次数用完，请求失败")
    return False

retry_request()

# 例子4：读取直到满足条件
def collect_until_stop():
    data = [1, 2, 3, "stop", 4]      # 模拟输入流
    result = []
    i = 0
    while i < len(data):
        if data[i] == "stop":
            break
        result.append(data[i])
        i += 1
    return result

print(collect_until_stop())          # [1, 2, 3]
