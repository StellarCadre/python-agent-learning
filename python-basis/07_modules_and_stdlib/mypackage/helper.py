# ============================================================
# mypackage/helper.py 工具模块
# ============================================================

def greet(name):
    return f"你好，{name}"

def calculate(a, b, op="+"):
    ops = {
        "+": lambda: a + b,
        "-": lambda: a - b,
        "*": lambda: a * b,
    }
    return ops.get(op, lambda: "未知运算符")()

# 模块级常量
DEFAULT_TIMEOUT = 30
