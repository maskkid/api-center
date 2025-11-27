from fastapi import APIRouter, Query, Response
from api_center.utils.response import success, error
import requests
from api_center.utils.decorators import decorate_requests

router = APIRouter(prefix="/gateway", tags=["gateway"])


@router.get('/config')
def get_gateway_config():
    """Get gateway configuration"""
    return success({"endpoints": ["user", "admin", "chat"]})


@router.get('/proxy')
def proxy(url: str = Query(..., description='URL to proxy')):
    if not url:
        return error("URL parameter is required", code=400)
    try:
        resp = decorate_requests(requests).get(url, timeout=10)
        content_type = resp.headers.get('Content-Type', 'application/octet-stream')
        return Response(content=resp.content, media_type=content_type)
    except Exception as e:
        return error(f"Proxy error: {str(e)}", code=500)
