# ============================================================
# sample_agent/tools/registry.py 工具注册中心（Function Calling）
# ============================================================
# 用装饰器把工具函数注册到字典，Agent 可根据模型返回的工具名调用。
# ============================================================

from typing import Callable, Any

# 工具注册表：工具名 -> {函数, 描述}
TOOL_REGISTRY: dict[str, dict[str, Any]] = {}


def register_tool(name: str, description: str = "") -> Callable:
    def decorator(func: Callable) -> Callable:
        TOOL_REGISTRY[name] = {
            "func": func,
            "description": description,
        }
        return func
    return decorator


def call_tool(name: str, **arguments) -> Any:
    """按名字调用工具"""
    if name not in TOOL_REGISTRY:
        raise KeyError(f"未知工具: {name}")
    return TOOL_REGISTRY[name]["func"](**arguments)
