# ============================================================
# HTTP 请求：httpx（同步）
# ============================================================
# Agent 调用大模型 API 本质就是发 HTTP 请求。
#
# 安装：pip install httpx
#
# Go 用 net/http 或 resty，Python 推荐 httpx：
#   - 同时支持同步和异步（API 一致）
#   - 支持 HTTP/2、超时、连接池
#   - requests 是老牌同步库，资料多，但不支持异步
#
# 注意：本文件中的真实请求需要联网，
# 为方便学习，主要用公开测试地址 httpbin.org 演示。
# ============================================================

import httpx

# ---------- 1. 最简单的 GET ----------

# httpx.get 是快捷方法（内部自动创建客户端）
# response = httpx.get("https://httpbin.org/get")
# print(response.status_code)
# print(response.text)               # 响应体文本

# 为避免无网络时报错，下面用 try 包裹，结构是标准写法
try:
    resp = httpx.get("https://httpbin.org/get", timeout=5)
    print("状态码:", resp.status_code)
    print("响应文本:", resp.text[:200])
except httpx.HTTPError as e:
    print("请求失败（可能无网络）:", e)

# ---------- 2. Response 对象常用属性/方法 ----------
#
#   resp.status_code   HTTP 状态码
#   resp.text          响应体（字符串，自动解码）
#   resp.content       响应体（bytes，二进制）
#   resp.json()        解析 JSON（返回 dict/list），解析失败抛异常
#   resp.headers       响应头（类 dict）
#   resp.encoding      编码
#   resp.url           最终 URL
#   resp.is_success    是否 2xx
#   resp.raise_for_status()  非成功状态码抛异常

# 解析 JSON 响应（Agent 最常用）
try:
    resp = httpx.get("https://httpbin.org/json", timeout=5)
    data = resp.json()               # JSON -> dict
    print("JSON数据:", data)
except httpx.HTTPError as e:
    print("失败:", e)

# ---------- 3. 查询参数 params ----------

# params 自动拼到 URL ?key=value（不用自己拼，自动处理编码）
try:
    resp = httpx.get(
        "https://httpbin.org/get",
        params={"q": "python", "page": 2, "tag": ["a", "b"]},  # 多值参数
        timeout=5,
    )
    print("最终URL:", resp.url)
except httpx.HTTPError as e:
    print("失败:", e)

# ---------- 4. POST 表单 / JSON ----------

# POST JSON（调模型 API 的标准方式）
try:
    resp = httpx.post(
        "https://httpbin.org/post",
        json={"model": "gpt-4", "messages": [{"role": "user", "content": "hi"}]},
        timeout=5,
    )
    print("POST状态:", resp.status_code)
except httpx.HTTPError as e:
    print("失败:", e)

# POST 表单（application/x-www-form-urlencoded）
# resp = httpx.post(url, data={"key": "value"})

# 区分：
#   json=  -> Content-Type: application/json（调 API 用）
#   data=  -> 表单提交
#   content= -> 原始 bytes/文本

# ---------- 5. 请求头 headers ----------

# resp = httpx.get(url, headers={"Authorization": "Bearer sk-xxx"})

# ---------- 6. 超时 timeout ----------

# httpx.get(url, timeout=10)                  # 统一10秒
# httpx.Client(timeout=httpx.Timeout(5.0, connect=2.0))

# 不设超时可能永久挂起，实际项目一定要设

# ---------- 7. 推荐用 Client（连接复用，生产环境）----------
# 快捷方法每次新建连接，Client 复用连接池（类似 Go 的 http.Client）

def client_demo():
    with httpx.Client(base_url="https://httpbin.org", timeout=5) as client:
        # 相对路径，自动拼 base_url
        r1 = client.get("/get")
        r2 = client.post("/post", json={"a": 1})
        print("Client复用:", r1.status_code, r2.status_code)

try:
    client_demo()
except httpx.HTTPError as e:
    print("失败:", e)
# with 自动关闭客户端，释放连接池

# ---------- 8. 错误处理（重要）----------

def robust_get(url):
    try:
        resp = httpx.get(url, timeout=5)
        resp.raise_for_status()       # 4xx/5xx 抛 HTTPStatusError
        return resp.json()
    except httpx.TimeoutException:
        print("超时")
    except httpx.ConnectError:
        print("连接失败")
    except httpx.HTTPStatusError as e:
        print(f"状态错误 {e.response.status_code}")
    except httpx.HTTPError as e:
        print("其他HTTP错误:", e)

print(robust_get("https://httpbin.org/get"))

# ---------- 9. 封装一个简单的 API 客户端（实战）----------

class SimpleAPIClient:
    def __init__(self, base_url, api_key=None, timeout=10):
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        self.client = httpx.Client(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
        )

    def get(self, path, **params):
        resp = self.client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    def post(self, path, json_body):
        resp = self.client.post(path, json=json_body)
        resp.raise_for_status()
        return resp.json()

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

# 使用（以大模型接口风格为例）：
# with SimpleAPIClient("https://api.openai.com", api_key="sk-xxx") as c:
#     result = c.post("/v1/chat/completions", {
#         "model": "gpt-4",
#         "messages": [{"role": "user", "content": "你好"}],
#     })
