# ============================================================
# sample_agent/services/agent.py Agent 核心业务逻辑（≈ Go service）
# ============================================================
# 这里演示一个最小 Agent 的结构。为零依赖可运行，
# 模型调用部分用模拟实现，真实场景替换为 httpx 调用即可。
# ============================================================

from config import settings
from schemas import Message, ChatRequest, ChatResponse
from tools import TOOL_REGISTRY, call_tool


class AgentService:
    def __init__(self):
        self.model = settings.model

    def _build_messages(self, req: ChatRequest) -> list[dict]:
        """组装 system + history + 最新问题"""
        messages = [Message("system", "你是一个乐于助人的助手").to_dict()]
        messages.extend(m.to_dict() for m in req.history)
        messages.append(Message("user", req.question).to_dict())
        return messages

    async def chat(self, req: ChatRequest) -> ChatResponse:
        """处理一次对话（真实实现为异步 httpx 调用大模型）"""
        messages = self._build_messages(req)

        # ===== 真实场景（伪代码）=====
        # async with httpx.AsyncClient(...) as client:
        #     resp = await client.post("/v1/chat/completions", json={
        #         "model": self.model, "messages": messages,
        #     })
        # answer = resp.json()["choices"][0]["message"]["content"]

        # ===== 模拟返回（保证无 key 也能跑通流程）=====
        answer = f"（模拟{self.model}回答）你问的是：{req.question}"
        return ChatResponse(answer=answer, model=self.model)

    def list_tools(self) -> dict:
        """列出可用工具"""
        return {
            name: meta["description"]
            for name, meta in TOOL_REGISTRY.items()
        }
