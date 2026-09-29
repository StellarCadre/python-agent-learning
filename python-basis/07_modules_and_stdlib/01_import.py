# ============================================================
# 模块导入（import）全面讲解
# ============================================================
# 一个 .py 文件就是一个模块（module），
# 含 __init__.py 的文件夹是包（package）。
#
# Go 导入：import "github.com/xxx/pkg"
# Python 导入：import 模块名 / from 模块 import 名字
#
# 运行本文件前，需要在 07_modules_and_stdlib 目录下运行，
# 或者把该目录加入 Python 路径（PyCharm 会自动处理）。
# ============================================================

# ---------- 1. import 整个模块 ----------

import math                           # 导入标准库 math
print(math.sqrt(16))                 # 使用时要加 模块名.

import os, sys, json                  # 一行导入多个模块（不推荐，PEP8建议分开）

# ---------- 2. from ... import 导入具体名字 ----------

from math import sqrt, pi            # 只导入需要的函数/常量
print(sqrt(25), pi)                  # 直接用，不用加 math.

from datetime import datetime        # 极高频
print(datetime.now())

# ---------- 3. as 起别名 ----------

import numpy as np                   # 约定俗成的别名（了解）
import pandas as pd

from datetime import datetime as dt  # 给具体名字起别名
print(dt.now())

# 别名用于避免命名冲突或简化长名字

# ---------- 4. from 模块 import * （不推荐）----------
# from math import *      # 导入所有公开名字，容易污染命名空间，不要用

# ---------- 5. 导入自己写的包 ----------
# mypackage 是当前目录下的包（含 __init__.py）

import mypackage                     # 导入包，执行 __init__.py
from mypackage import helper         # 导入包里的模块
print(helper.greet("Tom"))

from mypackage.helper import greet, calculate   # 直接导入函数
print(greet("Bob"))
print(calculate(3, 5, "*"))

from mypackage.models import User
u = User(1, "Alice")
print(u)

# ---------- 6. 相对导入（包内部模块之间）----------
# 在包内部可以用 . 表示当前包，.. 表示上级包：
#   from . import helper
#   from .models import User
#   from ..other_pkg import func
# 注意：相对导入只能在包内模块使用，直接运行脚本时不能用

# ---------- 7. 模块搜索路径 sys.path ----------
import sys
# Python 导入模块时按以下顺序查找：
#   1. 当前脚本所在目录
#   2. 环境变量 PYTHONPATH 中的目录
#   3. Python 安装目录的标准库
#   4. site-packages（第三方库）
print(sys.path)

# 坑：ModuleNotFoundError 通常是路径不对或没装包
# 不要让自己的文件名和标准库/第三方库重名！
# 比如新建 json.py 会导致 import json 导入你自己的文件（循环问题）

# ---------- 8. __name__ 与模块入口 ----------
# 每个模块有 __name__ 属性：
#   直接运行该文件时：__name__ == "__main__"
#   被 import 时：__name__ == 模块名
#
# 这是 Python 最经典的写法，相当于 Go 的 func main()

def main():
    print("这是程序主逻辑")

if __name__ == "__main__":
    main()
    print("只有直接运行本文件才执行，被 import 不执行")

# 好处：模块既可以独立运行，也可以被导入复用而不自动执行测试代码

# ---------- 9. 模块只导入一次 ----------
# 模块在第一次 import 时执行，之后重复 import 直接用缓存
import importlib
# importlib.reload(math)    # 强制重新加载（很少用）

# ---------- 10. 循环导入问题 ----------
# a.py import b，b.py import a 会报错 ImportError
# 解决：重构代码提取公共部分，或延迟导入（函数内 import）
# Go 也禁止循环依赖，理念相同
