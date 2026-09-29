# ============================================================
# sample_agent/tools/builtin.py 内置工具示例
# ============================================================

from .registry import register_tool


@register_tool("calculator", "执行简单的数学计算")
def calculator(expression: str) -> str:
    # 安全提示：eval 有注入风险，生产环境应使用安全解析库
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "表达式含非法字符"
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算失败: {e}"


@register_tool("current_time", "获取当前时间")
def current_time() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
