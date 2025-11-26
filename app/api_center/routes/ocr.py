from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
import logging
from api_center.utils.response import success, error
from api_center.vendors.ai_ocr import OCRService

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ocr", tags=["ocr"])


@router.get('/recognize')
def recognize_get(url: str = None, language: str = 'ch'):
    """通过URL识别图片文字（GET方法）"""
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter is required")
    try:
        result = OCRService.recognize_from_url(url, language)
        return success(result)
    except Exception as e:
        logger.error(f"OCR处理错误: {str(e)}")
        error_message = str(e)
        if "Failed to download image" in error_message:
            raise HTTPException(status_code=400, detail=error_message)
        raise HTTPException(status_code=500, detail=error_message)


@router.post('/recognize')
async def recognize_post(request: Request, file: UploadFile = File(None), language: str = Form('ch')):
    """通过文件上传或URL识别图片文字（POST方法）"""
    try:
        # 如果有 JSON body 并包含 url，则处理 URL 模式
        try:
            body = await request.json()
        except Exception:
            body = None

        if body and 'url' in body:
            url = body['url']
            lang = body.get('language', 'ch')
            result = OCRService.recognize_from_url(url, lang)
            return success(result)

        if file is None:
            raise HTTPException(status_code=400, detail='No file provided')

        # 处理文件上传
        content = await file.read()
        result = OCRService.recognize_from_file(content, language)
        return success(result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OCR处理错误: {str(e)}")
        error_message = str(e)
        if "Failed to download image" in error_message:
            raise HTTPException(status_code=400, detail=error_message)
        raise HTTPException(status_code=500, detail=error_message)


@router.get('/wx/recognize')
def wx_recognize_get(url: str = None, api_url: str = None):
    if not url:
        raise HTTPException(status_code=400, detail='URL parameter is required')
    try:
        result = OCRService.recognize_with_wx_from_url(url, api_url)
        return success(result)
    except Exception as e:
        logger.error(f"微信OCR处理错误: {str(e)}")
        error_message = str(e)
        if "Failed to download image" in error_message:
            raise HTTPException(status_code=400, detail=error_message)
        raise HTTPException(status_code=500, detail=error_message)


@router.post('/wx/recognize')
async def wx_recognize_post(request: Request, file: UploadFile = File(None), api_url: str = Form(None)):
    try:
        try:
            body = await request.json()
        except Exception:
            body = None

        if body and 'url' in body:
            url = body['url']
            api_url = body.get('api_url')
            result = OCRService.recognize_with_wx_from_url(url, api_url)
            return success(result)

        if file is None:
            raise HTTPException(status_code=400, detail='No file provided')

        content = await file.read()
        result = OCRService.recognize_with_wx_from_file(content, api_url)
        return success(result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"微信OCR处理错误: {str(e)}")
        error_message = str(e)
        if "Failed to download image" in error_message:
            raise HTTPException(status_code=400, detail=error_message)
        raise HTTPException(status_code=500, detail=error_message)
