"""API Center main FastAPI application"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import json

# import our FastAPI routers
from api_center.routes import user, admin, gateway, qrcode, chat, genimg, tts, asr, ocr


app = FastAPI(title="API Center")


@app.get("/", response_class=JSONResponse)
def root():
    return {"message": "Welcome to API Center (FastAPI)", "docs_url": "/docs", "api_prefix": "/api/v1"}


@app.get("/swagger.json", response_class=JSONResponse)
def swagger_json():
    docs_dir = os.path.join(os.path.dirname(__file__), 'docs')
    swagger_file = os.path.normpath(os.path.join(docs_dir, 'swagger.json'))
    if os.path.exists(swagger_file):
        try:
            with open(swagger_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return JSONResponse({"warning": "failed to read swagger.json"}, status_code=500)
    return JSONResponse({"warning": "swagger.json not found"}, status_code=404)


# Include FastAPI routers under /api/v1
app.include_router(user.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(gateway.router, prefix="/api/v1")
app.include_router(qrcode.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(genimg.router, prefix="/api/v1")
app.include_router(tts.router, prefix="/api/v1")
app.include_router(asr.router, prefix="/api/v1")
app.include_router(ocr.router, prefix="/api/v1")
