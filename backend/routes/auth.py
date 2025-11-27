from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from config import config
import jwt
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter(prefix="/auth", tags=["auth"])

def verify_token(token: str) -> bool:
    """
    验证管理员token
    """
    return token == config.admin_token


@router.post("/login")
def login(
    username: str,
    password: str,
    db: Session = Depends(get_db),
):
    """
    管理员登录
    """
    if username != config.admin_username or password != config.admin_password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 生成JWT token
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, config.admin_token, algorithm="HS256")
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": username
    }