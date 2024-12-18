# app/main.py
from fastapi import FastAPI, APIRouter
from database import engine, Base
from routers import script_security

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Test Script Management API",
    description="API for managing test scripts",
    version="1.0.0"
)
# 设置统一的 api 前缀
api_router = APIRouter(prefix="/api")
# 注册路由
# api_router.include_router(scripts.router)
# api_router.include_router(script_details.router)
api_router.include_router(script_security.router)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
