# ============================================================
# sample_agent/config.py 配置管理
# ============================================================
# 配置（API Key、模型名）从环境变量读取，不要写死提交到代码仓库。
# 对应 Go 项目的 config 包。
#
# 实际项目可安装 pydantic-settings：pip install pydantic-settings
# 这里用标准库 os 演示，零依赖。
# ============================================================

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # 大模型 API 配置
    api_base_url: str
    api_key: str
    model: str
    timeout: int
    temperature: float

    @classmethod
    def from_env(cls) -> "Settings":
        """从环境变量加载配置"""
        return cls(
            api_base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com"),
            api_key=os.getenv("LLM_API_KEY", ""),       # 必须在环境变量配置
            model=os.getenv("LLM_MODEL", "gpt-4"),
            timeout=int(os.getenv("LLM_TIMEOUT", "60")),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
        )


# 全局唯一配置实例
settings = Settings.from_env()
