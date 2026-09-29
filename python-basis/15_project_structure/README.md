# 示例 Agent 项目结构说明

这是一个**分层清晰、零框架依赖**的 Agent 项目骨架，展示 Python 工程化的标准组织方式，和你熟悉的 Go 分层（handler/service/model）一一对应。

## 目录结构

```
sample_agent/
├── main.py              # 程序入口（真实项目可换成 FastAPI）
├── config.py            # 配置，从环境变量读取（≈ Go config 包）
├── requirements.txt     # 依赖清单（≈ go.mod）
├── schemas/             # 数据模型，dataclass（≈ DTO/VO）
│   ├── __init__.py
│   └── chat.py
├── services/            # 业务/Agent 逻辑（≈ service 层）
│   ├── __init__.py
│   └── agent.py
├── tools/               # 工具函数，Function Calling
│   ├── __init__.py
│   ├── registry.py      # 工具注册中心
│   └── builtin.py       # 内置工具
└── utils/               # 通用工具函数（按需添加）
```

## 分层职责

| 层 | 职责 | Go 对应 |
|---|---|---|
| `main.py` | 启动程序、组装依赖 | main 函数 |
| `config.py` | 读取环境变量、集中配置 | config 包 |
| `schemas/` | 定义入参/出参数据结构 | DTO/VO struct |
| `services/` | 核心业务逻辑、编排模型和工具 | service 层 |
| `tools/` | 可被 Agent 调用的外部能力 | — |
| `utils/` | 与业务无关的通用函数 | utils 包 |

## 运行方式

```bash
# 1. 在 sample_agent 目录下执行
python main.py

# 2. 配置真实 API（PowerShell）
$env:LLM_API_KEY="sk-你的key"
$env:LLM_MODEL="gpt-4"
python main.py
```

## 关键工程约定

1. **配置与代码分离**：密钥只放环境变量或 `.env`，不写死、不提交。
2. **包标识**：每个作为包的文件夹放 `__init__.py`。
3. **入口判断**：`if __name__ == "__main__":` 防止被导入时误执行。
4. **依赖隔离**：每个项目用独立 conda/venv 环境。
5. **分层单向依赖**：`main -> services -> tools/schemas`，不反向依赖。
6. **异常分层处理**：底层抛具体异常，入口统一捕获转换。

## 后续演进

当基础打牢后，只需：
- 用 **FastAPI** 替换 `main.py`，把 `AgentService.chat` 暴露为 HTTP 接口
- 用 **Pydantic BaseModel** 替换 schemas 中的 dataclass（接口边界校验）
- 在 `services/agent.py` 中接入真实的 httpx 大模型调用和 RAG 流程

整体分层结构无需改动，这就是分层设计的价值。
