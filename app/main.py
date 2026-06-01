import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import chat
from app.api.v1 import oss
from app.common.logger import setup_logging, logger
from app.rag.vector_store import RecipeVectorStore
from app.rag.recipes_seed import SEED_RECIPES
from app.db import recipes_db
from app.skills import register_all_skills

# 初始化日志配置
setup_logging()


def _init_rag_knowledge_base():
    """Initialize RAG recipe knowledge base on startup."""
    # 1. Ensure recipes source-of-truth table exists
    recipes_db.create_table()

    # 2. If recipes table is empty, seed from hardcoded defaults
    if recipes_db.count() == 0:
        logger.info(f"recipes table empty, seeding {len(SEED_RECIPES)} default recipes...")
        n = recipes_db.seed_from_dicts(SEED_RECIPES)
        logger.info(f"recipes table seeded: {n} recipes inserted.")

    # 3. Sync vector index from recipes table
    db_path = os.path.join(os.path.dirname(__file__), "db", "personal_chief.db")
    store = RecipeVectorStore(
        db_path=db_path,
        base_url=os.getenv("DASHSCOPE_BASE_URL"),
        api_key=os.getenv("DASHSCOPE_API_KEY")
    )
    existing_vec = store.count()
    if existing_vec == 0:
        all_recipes = recipes_db.get_all_as_dicts()
        count = store.seed(all_recipes)
        logger.info(f"Vector index seeded with {count} recipes from recipes table.")
    else:
        logger.info(f"Vector index already has {existing_vec} recipes, skipping sync.")
    store.close()


_init_rag_knowledge_base()

# Register pluggable skills for the agent
register_all_skills()

app = FastAPI(
    title="Personal Chief API",
    description="私厨",
    version="0.1.0"
)

# 1. 配置跨域资源共享 (CORS)
# 插件开发中，由于请求来自浏览器扩展环境，必须正确配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议指定插件的 ID 或具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2.挂载路由
app.include_router(chat.router, prefix="/api/v1", tags=["对话"])
app.include_router(oss.router, prefix="/api/v1", tags=["申请上传签名url"])

# 延迟导入 recipes/skills 路由以避免循环引用
from app.api.v1.recipes import router as recipes_router  # noqa: E402
from app.api.v1.skills import router as skills_router  # noqa: E402
app.include_router(recipes_router, prefix="/api/v1", tags=["食谱管理"])
app.include_router(skills_router, prefix="/api/v1", tags=["技能管理"])
from app.api.v1.settings import router as settings_router  # noqa: E402
app.include_router(settings_router, prefix="/api/v1", tags=["设置"])

# 3.挂载前端资源
static_dir = os.path.join(os.path.dirname(__file__), "static")

# Admin page route (must be before catch-all)
@app.get("/admin/recipes", include_in_schema=False)
async def serve_admin_recipes():
    admin_path = os.path.join(static_dir, "admin", "recipes.html")
    if os.path.exists(admin_path):
        return FileResponse(admin_path)
    return JSONResponse({"error": "Admin page not found"}, status_code=404)

if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

# 前端 fallback 路由 - 只处理非 API 请求
@app.get("/{path:path}", include_in_schema=False)
async def serve_frontend(path: str):
    # 排除 API 路径
    if path.startswith("api/"):
        from fastapi.responses import JSONResponse
        return JSONResponse({"error": "Not Found"}, status_code=404)
    # 如果请求的是静态文件，直接返回
    file_path = os.path.join(static_dir, path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    # 否则返回 index.html（SPA fallback）
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "你的独家私厨上线了~", "status": "ok"}

if __name__ == "__main__":
    import uvicorn
    # 启动命令：python -m app.main
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
