# ============================================================
# Agent 开发常用标准库速览
# ============================================================
# 不用专门背，知道每个库干嘛、用到时查即可。
# ============================================================

# ---------- 1. os：操作系统交互 ----------
import os

print(os.getcwd())                    # 当前工作目录
print(os.environ.get("PATH"))         # 读取环境变量（配置/密钥常用）
os.environ.setdefault("MY_VAR", "dev")
# os.getenv("API_KEY", "默认值")      # 读环境变量（推荐）
# os.makedirs("a/b/c", exist_ok=True)  # 创建目录
# os.path.exists("文件")             # 判断存在
# os.remove / os.rename              # 删除/重命名

# ---------- 2. sys：解释器相关 ----------
import sys

print(sys.version)                   # Python 版本
# sys.argv        # 命令行参数列表（Go os.Args）
# sys.exit(0)     # 退出程序
# sys.path        # 模块搜索路径

# ---------- 3. pathlib：面向对象路径（推荐，比 os.path 现代）----------
from pathlib import Path

p = Path(".") / "data" / "test.txt"  # 用 / 拼接路径（跨平台）
print(p)
print(p.exists(), p.suffix, p.stem)  # 存在/后缀/文件名
# Path(".").glob("*.py")             # 查找文件
# p.read_text(encoding="utf-8")      # 直接读
# p.write_text("内容")               # 直接写
# p.mkdir(parents=True, exist_ok=True)

# ---------- 4. datetime 日期时间 ----------
from datetime import datetime, date, timedelta, timezone

now = datetime.now()
print(now, now.strftime("%Y-%m-%d %H:%M"))
today = date.today()
tomorrow = today + timedelta(days=1)
print(tomorrow)
parsed = datetime.strptime("2026-09-28", "%Y-%m-%d")
print(parsed)

# ---------- 5. time 时间 ----------
import time

print(time.time())                   # 当前时间戳（秒）
# time.sleep(1)                      # 暂停1秒

# ---------- 6. logging 日志 ----------
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logging.info("普通信息")
logging.warning("警告")
logging.error("错误")
# 级别：DEBUG < INFO < WARNING < ERROR < CRITICAL

# ---------- 7. re 正则表达式 ----------
import re

result = re.findall(r"\d+", "a1b22c333")
print(result)                        # ['1','22','333']
match = re.search(r"(\w+)@(\w+)", "email a@b here")
if match:
    print(match.group(0), match.groups())
print(re.sub(r"\s+", "-", "a b  c"))  # a-b-c

# ---------- 8. random 随机 ----------
import random

print(random.randint(1, 100))        # 随机整数
print(random.choice(["a", "b", "c"]))
random.shuffle(result if False else [1, 2, 3])

# ---------- 9. json（下个文件夹专门讲）----------

# ---------- 10. dataclasses（类型注解章节讲）----------

# ---------- 11. functools / itertools（函数章节讲过）----------

# ---------- 12. typing（类型注解章节讲）----------

# ---------- 13. textwrap / string 等文本工具 ----------
import textwrap
print(textwrap.shorten("这是一段非常非常长的文本", width=10, placeholder="..."))

# ---------- 14. hashlib / uuid ----------
import hashlib, uuid

print(hashlib.md5("hello".encode()).hexdigest())
print(uuid.uuid4())                  # 生成唯一ID

# ---------- 15. subprocess（执行外部命令，谨慎用）----------
# import subprocess
# subprocess.run(["python", "--version"])

# ---------- 16. collections.abc 抽象类型 ----------
from collections.abc import Mapping, Sequence
# 用于类型判断和接口定义
