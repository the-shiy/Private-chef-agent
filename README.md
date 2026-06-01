# Private Chef Agent

AI 私人厨师助手，支持通过食材图片或文字对话发现菜谱。基于 FastAPI + LangGraph 构建，使用 RAG 本地向量数据库，搭配 Tavily 网络搜索增强。

## 技术栈

- **后端**: FastAPI + Uvicorn
- **AI**: LangGraph / LangChain + DashScope (Qwen3-Omni-Flash)
- **向量检索**: SQLite-vec (1024 维 embedding)
- **对话记忆**: LangGraph Checkpoint (SQLite)
- **图片上传**: 阿里云 OSS
- **前端**: Next.js 静态导出 (app/static/)

## 前置条件

- Python >= 3.11
- [DashScope API Key](https://dashscope.console.aliyun.com/)（阿里云模型服务，LLM + Embedding）
- [Tavily API Key](https://tavily.com/)（网络搜索，可选）
- 阿里云 OSS Bucket（图片上传，可选）

## 环境变量

在 `app/` 目录下创建 `.env` 文件：

```env
# DashScope（必填）
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx

# Tavily 网络搜索（可选，不填则仅使用本地菜谱库）
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxx

# 阿里云 OSS 图片上传（可选）
OSS_BUCKET=your-bucket-name
OSS_ACCESS_KEY_ID=LTAI5t...
OSS_ACCESS_KEY_SECRET=...
# OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com  # 默认值
```

## 安装与运行

```bash
# 1. 克隆仓库
git clone git@github.com:the-shiy/Private-chef-agent.git
cd Private-chef-agent

# 2. 安装依赖
pip install -e .

# 3. 安装 sqlite-vec 扩展（向量检索所需）
pip install sqlite-vec

# 4. 创建 .env 文件（见上方模板）
# 放在 app/.env

# 5. 启动服务
python -m app.main
```

服务启动后访问 `http://127.0.0.1:8001`。

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/chat/stream` | 流式对话（AI 厨师） |
| GET | `/api/v1/chat/messages?thread_id=` | 获取对话历史 |
| DELETE | `/api/v1/chat/messages?thread_id=` | 清空对话历史 |
| GET | `/api/v1/recipes` | 菜谱列表/搜索 |
| GET | `/api/v1/recipes/{id}` | 菜谱详情 |
| POST | `/api/v1/recipes` | 创建菜谱 |
| PUT | `/api/v1/recipes/{id}` | 更新菜谱 |
| DELETE | `/api/v1/recipes/{id}` | 删除菜谱 |
| GET | `/api/v1/skills` | 技能列表 |
| POST | `/api/v1/skills/{name}/toggle` | 启用/禁用技能 |
| GET | `/api/v1/oss/presign?filename=` | 获取 OSS 上传链接 |
| GET | `/api/v1/settings` | 获取设置 |
| POST | `/api/v1/settings/web-search` | 切换网络搜索 |
| GET | `/admin/recipes` | 管理后台页面 |
| GET | `/` | 前端界面 |

## 项目结构

```
app/
├── main.py              # 入口，FastAPI 应用
├── langgraph.json        # LangGraph 配置
├── agents/               # AI Agent（厨师对话）
├── api/v1/               # REST API 路由
├── skills/               # 技能模块（营养分析、购物清单等）
├── rag/                  # RAG 向量检索 + 种子菜谱
├── db/                   # SQLite 数据库层
├── models/               # Pydantic 数据模型
├── static/               # Next.js 前端静态文件
└── common/               # 日志等公共模块
```
