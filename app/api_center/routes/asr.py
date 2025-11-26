from fastapi import APIRouter
from api_center.utils.response import success

router = APIRouter(prefix="/asr", tags=["asr"])


@router.post('/recognize')
def recognize_speech(payload: dict):
    """Recognize speech (mock)"""
    return success({"transcript": "这是识别出的文字内容"})
