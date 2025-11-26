from fastapi import APIRouter, Query, Response
from api_center.utils.response import success, error
import qrcode
from io import BytesIO
import base64

router = APIRouter(prefix="/qrcode", tags=["qrcode"])


def _make_qrcode_bytes(content: str, box_size: int = 10, border: int = 4) -> bytes:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.getvalue()


@router.get('/generate')
def generate_qrcode_get(
    content: str = Query(..., description='Content to encode in QR code'),
    box_size: int = Query(10, description='Size of each box in pixels'),
    border: int = Query(4, description='Border size in boxes'),
    format: str = Query('base64', description='Response format (base64 or png)')
):
    """Generate QR Code using GET method"""
    if not content:
        return error("Content parameter is required", code=400)

    try:
        img_bytes = _make_qrcode_bytes(content, box_size, border)
        if format.lower() == 'png':
            return Response(content=img_bytes, media_type='image/png')
        else:
            img_str = base64.b64encode(img_bytes).decode()
            return success({'format': 'base64', 'data': f'data:image/png;base64,{img_str}'})
    except Exception as e:
        return error(f"Error generating QR code: {str(e)}", code=500)


@router.post('/generate')
def generate_qrcode_post(payload: dict):
    """Generate QR Code using POST method"""
    if not payload or 'content' not in payload:
        return error("Content is required in request body", code=400)

    content = payload['content']
    box_size = int(payload.get('box_size', 10))
    border = int(payload.get('border', 4))
    response_format = payload.get('format', 'base64')

    try:
        img_bytes = _make_qrcode_bytes(content, box_size, border)
        if response_format.lower() == 'png':
            return Response(content=img_bytes, media_type='image/png')
        else:
            img_str = base64.b64encode(img_bytes).decode()
            return success({'format': 'base64', 'data': f'data:image/png;base64,{img_str}'})
    except Exception as e:
        return error(f"Error generating QR code: {str(e)}", code=500)
