from fastapi import APIRouter
from api_center.utils.response import success

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get('/dashboard')
def dashboard():
    """Get admin dashboard data"""
    return success({"stats": {"users": 100, "requests": 5000}})
