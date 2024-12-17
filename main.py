# app/main.py
from fastapi import FastAPI
from .database import engine, Base
from .routers import scripts, script_details

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Test Script Management API",
    description="API for managing test scripts",
    version="1.0.0"
)

# 注册路由
app.include_router(scripts.router)
app.include_router(script_details.router)
