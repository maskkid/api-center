"""FastAPI routers package initializer.

Each module exposes a `router` variable (APIRouter) so the main
application can `include_router(...)`.
"""
from . import user, admin, gateway, qrcode, chat, genimg, tts, asr, ocr

__all__ = [
    'user', 'admin', 'gateway', 'qrcode', 'chat',
    'genimg', 'tts', 'asr', 'ocr'
]
