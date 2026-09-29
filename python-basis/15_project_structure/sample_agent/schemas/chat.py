# ============================================================
# sample_agent/schemas/chat.py 数据模型（≈ Go 的 DTO/VO）
# ============================================================

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class Message:
    """聊天消息"""
    role: Literal["system", "user", "assistant"]
    content: str

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}


@dataclass
class ChatRequest:
    """入参：用户问题"""
    question: str
    history: list[Message] = field(default_factory=list)


@dataclass
class ChatResponse:
    """出参：模型回答"""
    answer: str
    model: str
