from fastapi import APIRouter
from api_center.utils.response import success

router = APIRouter(prefix="/genimg", tags=["genimg"])


@router.post('/generate')
def generate_image(payload: dict):
    """Generate image (mock)"""
    return success({"image_url": "https://example.com/generated_image.jpg"})
