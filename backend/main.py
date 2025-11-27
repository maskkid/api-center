from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from routes import shares, resources, auth, frontend, proxy
from config import config
from database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时的操作
    print("🚀 QuickPush Backend 启动中...")
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    yield
    # 关闭时的操作
    print("👋 QuickPush Backend 关闭中...")


# 创建FastAPI应用
app = FastAPI(
    title="QuickPush Backend",
    description="文案分享和管理后端服务",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该配置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(shares.router, prefix="/api/shares", tags=["分享管理"])
app.include_router(resources.router, prefix="/api/resources", tags=["资源管理"])
app.include_router(auth.router, prefix="/api/auth", tags=["认证管理"])
app.include_router(proxy.router, prefix="/api/proxy", tags=["代理服务"])
app.include_router(frontend.router, tags=["前端页面"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "QuickPush Backend 服务运行中",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "quickpush-backend"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )