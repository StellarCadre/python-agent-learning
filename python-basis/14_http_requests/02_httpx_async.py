# ============================================================
# HTTP 请求：httpx（异步，Agent 服务推荐）
# ============================================================
# 异步服务中必须用 AsyncClient，不能用同步 client（会阻塞事件循环）。
# 用 async with 管理客户端生命周期。
# ============================================================

import asyncio
import httpx

# ---------- 1. 异步 GET ----------

async def async_get():
    async with httpx.AsyncClient(timeout=5) as client:
        resp = await client.get("https://httpbin.org/get")
        print("状态:", resp.status_code)
        data = resp.json()
        print("数据:", str(data)[:100])

try:
    asyncio.run(async_get())
except httpx.HTTPError as e:
    print("请求失败:", e)

# 注意：
# 1. AsyncClient 的方法都要 await
# 2. 用 async with 自动关闭
# 3. client 尽量复用（不要每个请求新建）

# ---------- 2. 异步并发请求多个接口（核心优势）----------

async def fetch_one(client, name, delay_url):
    resp = await client.get(delay_url)
    return f"{name}:{resp.status_code}"

async def concurrent_requests():
    async with httpx.AsyncClient(timeout=10) as client:
        # 用 gather 并发，比顺序快
        results = await asyncio.gather(
            client.get("https://httpbin.org/get"),
            client.get("https://httpbin.org/uuid"),
            client.get("https://httpbin.org/json"),
            return_exceptions=True,
        )
        for r in results:
            if isinstance(r, Exception):
                print("失败:", r)
            else:
                print("并发结果状态:", r.status_code)

try:
    asyncio.run(concurrent_requests())
except Exception as e:
    print("失败:", e)

# ---------- 3. 异步 POST（调模型）----------

async def call_chat():
    async with httpx.AsyncClient(
        base_url="https://httpbin.org",
        timeout=30,
        headers={"Authorization": "Bearer sk-xxx"},
    ) as client:
        payload = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "你好"}],
            "temperature": 0.7,
        }
        resp = await client.post("/post", json=payload)
        print("调用状态:", resp.status_code)

try:
    asyncio.run(call_chat())
except httpx.HTTPError as e:
    print("失败:", e)

# ---------- 4. 异步流式响应（LLM streaming 关键）----------
# 大模型流式返回 SSE，用 client.stream 逐块读取

async def stream_demo():
    async with httpx.AsyncClient(timeout=10) as client:
        # client.stream 上下文方式
        async with client.stream("GET", "https://httpbin.org/stream/3") as resp:
            async for line in resp.aiter_lines():
                if line.strip():
                    print("流式行:", line[:80])

try:
    asyncio.run(stream_demo())
except httpx.HTTPError as e:
    print("失败:", e)

# 常用流式方法：
#   resp.aiter_bytes()   逐块 bytes
#   resp.aiter_text()    逐块文本
#   resp.aiter_lines()   逐行
#   resp.aiter_raw()     原始字节

# ---------- 5. 异步 API 客户端封装（实战模板）----------

class AsyncLLMClient:
    def __init__(self, base_url, api_key, timeout=60):
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )

    async def chat(self, messages, model="gpt-4", **options):
        payload = {"model": model, "messages": messages}
        payload.update(options)
        resp = await self.client.post("/v1/chat/completions", json=payload)
        resp.raise_for_status()
        return resp.json()

    async def chat_stream(self, messages, model="gpt-4"):
        payload = {"model": model, "messages": messages, "stream": True}
        async with self.client.stream(
            "POST", "/v1/chat/completions", json=payload
        ) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if line.startswith("data:"):
                    yield line[5:].strip()   # 生成器，逐段产出

    async def aclose(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.aclose()

# 使用：
# async def main():
#     async with AsyncLLMClient("https://api.openai.com", "sk-xxx") as c:
#         result = await c.chat([{"role":"user","content":"你好"}])
#         async for chunk in c.chat_stream([...]):
#             print(chunk)
# asyncio.run(main())
