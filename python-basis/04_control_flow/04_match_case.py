# ============================================================
# match-case 结构化模式匹配（Python 3.10+）
# ============================================================
# Go 的 switch：
#   switch status {
#   case 200: ...
#   case 404, 500: ...
#   default: ...
#   }
#
# Python 3.10 新增 match-case，比传统 switch 强大很多，
# 不仅能匹配值，还能匹配结构（解构列表、dict、类等）。
# ============================================================

# ---------- 1. 基本值匹配（类似 switch）----------

status = 404

match status:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case 500:
        print("Server Error")
    case _:                           # _ 是通配符，相当于 default
        print("未知状态")

# 多个值合并（Go: case 401, 403:）
http_code = 401
match http_code:
    case 200 | 201 | 204:
        print("成功")
    case 401 | 403:
        print("无权限")
    case 404:
        print("未找到")
    case _:
        print("其他")

# ---------- 2. 匹配字符串 ----------

command = "start"

match command:
    case "start":
        print("启动")
    case "stop":
        print("停止")
    case "restart":
        print("重启")
    case _:
        print("未知命令")

# ---------- 3. 解构列表（强大功能）----------
# 不仅匹配值，还能绑定变量

point = [1, 2]

match point:
    case [0, 0]:
        print("原点")
    case [x, 0]:
        print(f"在x轴上，x={x}")
    case [0, y]:
        print(f"在y轴上，y={y}")
    case [x, y]:
        print(f"普通点 ({x}, {y})")
    case _:
        print("不是二维点")

# 匹配不定长列表
items = [1, 2, 3, 4]

match items:
    case [first]:
        print(f"只有一个元素: {first}")
    case [first, second]:
        print(f"两个元素: {first}, {second}")
    case [first, *rest]:              # *rest 收集剩余
        print(f"第一个: {first}, 剩余: {rest}")

# ---------- 4. 解构 dict ----------

response = {"status": "success", "data": {"id": 1, "name": "Tom"}, "code": 200}

match response:
    case {"status": "success", "data": data}:
        print("成功，数据:", data)
    case {"status": "error", "message": msg}:
        print("错误:", msg)
    case _:
        print("其他响应")

# 注意：dict 匹配只要求包含列出的 key，多余 key 不影响
# （和 list 不同，list 要匹配结构）

# ---------- 5. 匹配类对象 ----------

class Animal:
    def __init__(self, species, sound):
        self.species = species
        self.sound = sound

dog = Animal("狗", "汪")

match dog:
    case Animal(species="猫", sound=sound):
        print(f"猫叫{sound}")
    case Animal(species=sp, sound=sound):
        print(f"{sp}叫{sound}")

# ---------- 6. 守卫条件（case 后加 if）----------

point = (3, 4)

match point:
    case (x, y) if x == y:
        print("在对角线上")
    case (x, y) if x > y:
        print("x 大于 y")
    case (x, y):
        print(f"({x}, {y})")

# ---------- 7. 实战小例子 ----------

# 例子1：处理 API 响应
def handle_response(resp):
    match resp:
        case {"code": 200, "result": result}:
            return ("ok", result)
        case {"code": code, "error": msg} if code >= 500:
            return ("server_error", msg)
        case {"code": code, "error": msg} if code >= 400:
            return ("client_error", msg)
        case _:
            return ("unknown", None)

print(handle_response({"code": 200, "result": [1, 2]}))
print(handle_response({"code": 404, "error": "not found"}))

# 例子2：简单的命令解析
def parse_command(cmd_str):
    parts = cmd_str.split()
    match parts:
        case ["help"]:
            return "显示帮助"
        case ["get", key]:
            return f"获取 {key}"
        case ["set", key, value]:
            return f"设置 {key}={value}"
        case ["delete", key]:
            return f"删除 {key}"
        case ["exit"]:
            return "退出"
        case _:
            return "未知命令"

print(parse_command("set name Tom"))
print(parse_command("get name"))

# 例子3：处理不同类型的输入
def process(value):
    match value:
        case None:
            return "空值"
        case bool() as b:             # 注意 bool 要在 int 前面（bool 是 int 子类）
            return f"布尔 {b}"
        case int() as n:
            return f"整数 {n}"
        case str() as s:
            return f"字符串 {s}"
        case [x, y]:
            return f"二元列表 {x},{y}"
        case _:
            return "其他"

print(process(True))
print(process(42))
print(process("hi"))
