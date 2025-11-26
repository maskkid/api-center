from fastapi import APIRouter
from api_center.utils.response import success

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post('/send')
def send_message(payload: dict):
    """Send chat message (mock)"""
    return success({"reply": "This is a response from the AI assistant"})
