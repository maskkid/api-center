from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Optional
from api_center.utils.response import success, error

router = APIRouter(prefix="/user", tags=["user"])


class LoginIn(BaseModel):
    username: str
    password: str


class RegisterIn(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    phone: Optional[str] = None


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    phone: Optional[str] = None
    points: int


@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(payload: RegisterIn):
    """Create a new user (mock implementation)"""
    return success(msg="User registered successfully")


@router.post('/login')
def login(payload: LoginIn):
    """Login with existing credentials (mock)"""
    return success(msg="Login successful")


@router.get('/profile', response_model=dict)
def profile():
    """Get user profile information (mock)"""
    user_data = {
        "id": 1,
        "username": "test_user",
        "email": "test@example.com",
        "phone": "1234567890",
        "points": 100
    }
    return success(user_data)
