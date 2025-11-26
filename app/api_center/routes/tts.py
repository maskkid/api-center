from fastapi import APIRouter
from api_center.utils.response import success

router = APIRouter(prefix="/tts", tags=["tts"])


@router.post('/convert')
def convert_text(payload: dict):
    """Convert text to speech (mock)"""
    return success({"audio_url": "https://example.com/speech.mp3"})
