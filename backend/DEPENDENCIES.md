# Backend 依赖文档

## 概述
- 运行环境：建议 Python >= 3.8
- 安装方式：`pip install -r backend/requirements.txt`
- 说明：本文件根据当前源码实际导入与 `requirements.txt` 清单整理，标注缺失与可选项，便于维护与升级。

## 核心运行依赖
- fastapi：Web 框架（源码：main.py、routes/*）
- uvicorn[standard]：ASGI 服务器（源码：main.py）
- pydantic：数据模型与校验（源码：schemas.py、部分路由）
- sqlalchemy：ORM/数据库访问（源码：models.py、database.py、routes/*）
  - 数据库驱动：`PyMySQL`（配置 `mysql+pymysql://`，文件 `backend/config/settings.py:32`）
- httpx：HTTP 客户端（源码：routes/proxy.py）
- python-multipart：表单/文件上传支持（FastAPI 上传）
- pillow：图像处理（源码：routes/images.py 使用 PIL）
- python-dotenv：环境变量加载（配置）
- passlib[bcrypt]：密码哈希（认证相关）
- python-jose[cryptography]：加密与 JWT 支持（如使用 `from jose import jwt`）

## 缺失或需校准的依赖
- PyJWT：源码存在 `import jwt`（文件：`backend/routes/auth.py`），当前清单未包含 `PyJWT`。
  - 方案 A：改代码为 `from jose import jwt`，继续使用 `python-jose`（无需新增依赖）。
  - 方案 B：保留 `import jwt`，在 `requirements.txt` 添加 `PyJWT`。
- redis / aioredis：
  - 说明：`redis>=4` 已支持 asyncio，`aioredis` 为历史兼容包；建议择一保留，减少重复。
- celery、alembic：当前源码未直接导入，建议标注为“可选/运维工具”，需要时再启用。

## 当前 requirements.txt（原样引用）
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
httpx==0.25.2
redis==5.0.1
sqlalchemy==2.0.23
alembic==1.12.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
pillow==10.1.0
aiofiles==23.2.1
aioredis==2.0.1
celery==5.3.4
requests==2.31.0
```

## 安装与更新指引
- 安装：`pip install -r backend/requirements.txt`
- 升级流程：
  - 在分支中更新版本 → 跑单元测试/集成测试 → 回归关键路径（认证、上传、代理、数据库）→ 合并。
- 版本注意：
  - FastAPI 与 Pydantic v2 兼容性：已使用 Pydantic 2.x，升级 FastAPI 时注意 Breaking Changes。
  - SQLAlchemy 2.x API：保持 2.x 风格（Session/ORM 使用），升级需观察迁移脚本兼容。

## 可选开发依赖（不包含在运行依赖中）
- pytest：测试框架
- black、isort：代码格式化
- mypy：类型检查

## 维护建议
- 严格按照源码导入维护依赖清单，移除未使用的依赖，减少体积与安全面。
- 若启用 Celery、Alembic 或 Redis 队列等功能，请在此文档与 requirements 中同步更新说明。
