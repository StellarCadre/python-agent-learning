# ============================================================
# JSON 处理（Agent 开发极高频）
# ============================================================
# Go 用 encoding/json，通过 struct tag 映射：
#   json.Marshal / json.Unmarshal
#
# Python 用 json 模块，dict/list 和 JSON 天然对应：
#   json.dumps  -> dict 转 JSON 字符串（序列化，dump string）
#   json.loads  -> JSON 字符串转 dict（反序列化，load string）
#   json.dump   -> 写入文件
#   json.load   -> 从文件读取
# ============================================================

import json
from pathlib import Path

# ---------- 1. Python 类型与 JSON 类型对应 ----------
#
#   Python          JSON
#   dict            {} 对象
#   list / tuple    [] 数组
#   str             "字符串"
#   int / float     数字
#   True/False      true/false
#   None            null

# ---------- 2. 序列化：dumps ----------

data = {
    "name": "Tom",
    "age": 18,
    "is_vip": True,
    "score": 95.5,
    "tags": ["python", "agent"],
    "address": None,
}

# 基本序列化
json_str = json.dumps(data)
print(json_str)

# 坑1：默认 ensure_ascii=True，中文会被转义成 \uXXXX
data_cn = {"city": "北京", "msg": "你好"}
print(json.dumps(data_cn))                        # {"city": "\u5317\u4eac", ...}
print(json.dumps(data_cn, ensure_ascii=False))    # 中文正常显示（推荐）

# 美化输出（写文件/调试用）
pretty = json.dumps(data, ensure_ascii=False, indent=2)
print(pretty)

# 排序 key
print(json.dumps(data, sort_keys=True))

# 分隔符（紧凑输出，省空间）
print(json.dumps(data, separators=(",", ":")))

# ---------- 3. 反序列化：loads ----------

api_response = '{"id": 1, "name": "Tom", "roles": ["admin", "user"], "active": true, "note": null}'

obj = json.loads(api_response)
print(obj)                           # dict
print(obj["name"], obj["roles"][0])

# 坑：JSON 数字默认可能转 int 或 float
print(type(json.loads("10")))        # int
print(type(json.loads("10.0")))      # float

# 处理解析失败
bad_json = '{"name": "Tom", }'       # 尾随逗号，非法
try:
    json.loads(bad_json)
except json.JSONDecodeError as e:
    print("JSON解析失败:", e)

# ---------- 4. JSON 文件读写 ----------

config = {
    "model": "gpt-4",
    "temperature": 0.7,
    "messages": [{"role": "user", "content": "你好"}],
}

# 写入 JSON 文件
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

# 读取 JSON 文件
with open("config.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded["model"])

# pathlib 配合
Path("config2.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
loaded2 = json.loads(Path("config2.json").read_text(encoding="utf-8"))

# ---------- 5. 自定义对象的序列化（重要）----------
# 默认 json 不能直接序列化自定义类的实例

class User:
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

u = User(1, "Tom")
# json.dumps(u)                       # TypeError: not JSON serializable

# 方法1：转成 dict 再序列化
print(json.dumps({"uid": u.uid, "name": u.name}, ensure_ascii=False))

# 方法2：default 参数指定转换函数
def user_default(obj):
    if isinstance(obj, User):
        return {"uid": obj.uid, "name": obj.name}
    raise TypeError(f"无法序列化 {type(obj)}")

print(json.dumps(u, default=user_default, ensure_ascii=False))

# 方法3：类里提供转换方法
class User2:
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

    def to_dict(self):
        return self.__dict__          # __dict__ 是实例属性字典

print(json.dumps(User2(2, "Bob").to_dict(), ensure_ascii=False))

# 实际项目中用 Pydantic 的 BaseModel，序列化更方便（后面会讲）

# ---------- 6. 反序列化为自定义对象 ----------

# object_hook：每个 JSON 对象都会经过该函数
def user_hook(d):
    if "uid" in d and "name" in d:
        return User(d["uid"], d["name"])
    return d

result = json.loads('{"uid": 5, "name": "Alice"}', object_hook=user_hook)
print(result, type(result))

# ---------- 7. 实战小例子 ----------

# 例子1：模拟处理 LLM 的工具调用（Agent 核心场景）
tool_call_json = '''
{
  "tool": "search",
  "arguments": {"query": "Python教程", "limit": 3}
}
'''
call = json.loads(tool_call_json)
print("调用工具:", call["tool"])
print("参数:", call["arguments"]["query"])

# 例子2：合并多个 JSON 配置
def merge_json_files(*paths):
    result = {}
    for path in paths:
        with open(path, encoding="utf-8") as f:
            result.update(json.load(f))
    return result

# 例子3：JSONL（每行一个JSON，数据集/日志常用）
def write_jsonl(records, path):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def read_jsonl(path):
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records

write_jsonl([{"id": 1}, {"id": 2}], "data.jsonl")
print(read_jsonl("data.jsonl"))

# 清理
for tmp in ["config.json", "config2.json", "data.jsonl"]:
    Path(tmp).unlink(missing_ok=True)
