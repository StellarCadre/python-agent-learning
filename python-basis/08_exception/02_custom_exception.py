# ============================================================
# 自定义异常
# ============================================================
# Go 中可以自定义错误类型（实现 error 接口）：
#   type AppError struct { Code int; Msg string }
#   func (e *AppError) Error() string { return e.Msg }
#
# Python 自定义异常：继承 Exception（或更具体的内置异常）。
# 好处：可以携带业务信息、被针对性捕获、错误类型语义清晰。
# ============================================================

# ---------- 1. 最简单的自定义异常 ----------

class AgentError(Exception):
    """所有 Agent 相关错误的基类"""
    pass

# 抛出和捕获
try:
    raise AgentError("Agent 执行出错")
except AgentError as e:
    print("捕获:", e)

# ---------- 2. 带错误码和上下文的异常 ----------

class APIError(Exception):
    def __init__(self, message, status_code=500, response=None):
        # 调用父类初始化
        super().__init__(message)
        self.status_code = status_code
        self.response = response

    def __str__(self):
        return f"[HTTP {self.status_code}] {self.args[0]}"

try:
    raise APIError("请求失败", status_code=503, response={"retry": True})
except APIError as e:
    print(e)
    print("状态码:", e.status_code, "响应:", e.response)

# ---------- 3. 异常层级体系（项目中推荐的设计）----------

class AppBaseError(Exception):
    """项目异常基类"""
    def __init__(self, message="应用错误", code=None):
        super().__init__(message)
        self.code = code

class ConfigError(AppBaseError):
    """配置错误"""

class ModelError(AppBaseError):
    """模型调用错误"""
    def __init__(self, message, model=None, status_code=None):
        super().__init__(message, code=status_code)
        self.model = model

class ToolError(AppBaseError):
    """工具执行错误"""
    def __init__(self, tool_name, message):
        super().__init__(message)
        self.tool_name = tool_name

class RateLimitError(ModelError):
    """限流错误（更具体）"""
    def __init__(self, retry_after=1):
        super().__init__("请求过于频繁，被限流", status_code=429)
        self.retry_after = retry_after

# 可以分层捕获
def handle(error):
    if isinstance(error, RateLimitError):
        print(f"限流，{error.retry_after}秒后重试")
    elif isinstance(error, ModelError):
        print(f"模型 {error.model} 错误: {error}")
    elif isinstance(error, AppBaseError):
        print(f"业务错误(code={error.code}): {error}")
    else:
        print(f"未知错误: {error}")

handle(RateLimitError(retry_after=5))
handle(ModelError("超时", model="gpt-4"))
handle(ToolError("search", "搜索失败"))

# ---------- 4. 实战：Agent 执行中的异常处理 ----------

class BaseTool:
    def run(self, **kwargs):
        raise NotImplementedError

def execute_tool(tool, **kwargs):
    """统一执行工具并转换异常"""
    try:
        return tool.run(**kwargs)
    except ToolError:
        raise                            # 已经是业务异常，直接抛
    except (KeyError, TypeError) as e:
        # 把底层异常包装成语义清晰的业务异常
        raise ToolError(tool.__class__.__name__, f"参数错误: {e}") from e
    except Exception as e:
        raise ToolError(tool.__class__.__name__, f"工具执行失败: {e}") from e

class WeatherTool(BaseTool):
    def run(self, city=None, **kwargs):
        if not city:
            raise ToolError("WeatherTool", "缺少 city 参数")
        return f"{city}: 晴"

print(execute_tool(WeatherTool(), city="北京"))

try:
    execute_tool(WeatherTool())
except ToolError as e:
    print("捕获业务异常:", e.tool_name, e)

# ---------- 5. 最佳实践 ----------
# 1. 自定义异常名字以 Error 结尾
# 2. 建立项目异常基类，再按模块细分
# 3. 异常信息要清晰，说明"出了什么问题、怎么解决"
# 4. 不要用异常做正常流程控制（性能和可读性）
# 5. 边界层（如服务入口）统一捕获并转换，内部抛出具体异常
