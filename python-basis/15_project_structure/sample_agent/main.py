# ============================================================
# sample_agent/main.py 程序入口
# ============================================================
# 运行：python main.py
# 真实项目这里可以换成 FastAPI 暴露 HTTP 接口（本示例不涉及）。
# ============================================================

import asyncio

from schemas import ChatRequest
from services import AgentService


async def main():
    agent = AgentService()

    # 查看注册的工具
    print("可用工具:", agent.list_tools())

    # 发起一次对话
    req = ChatRequest(question="你好，介绍一下你自己")
    resp = await agent.chat(req)
    print("回答:", resp.answer)
    print("模型:", resp.model)


if __name__ == "__main__":
    asyncio.run(main())
