from fastapi import APIRouter
from api_center.utils.response import success

router = APIRouter(prefix="/gateway", tags=["gateway"])


@router.get('/config')
def get_gateway_config():
    """Get gateway configuration"""
    return success({"endpoints": ["user", "admin", "chat"]})
