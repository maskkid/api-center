from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
from pydantic import BaseModel
import base64
import io
from PIL import Image
import uuid
import os
from datetime import datetime

router = APIRouter()

class ImageUploadResponse(BaseModel):
    image_id: str
    image_url: str
    width: int
    height: int
    size: int
    format: str

class ImageProcessRequest(BaseModel):
    image_id: str
    operation: str  # resize, crop, rotate, filter
    params: dict

class CollageRequest(BaseModel):
    template: str  # grid2, grid3, grid4, grid6, grid9
    images: List[str]  # 图片URL列表
    spacing: int = 10
    background_color: str = "#FFFFFF"

# 模拟图片存储
IMAGE_DATA = {}
UPLOAD_DIR = "./uploads"

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """
    上传图片
    """
    # 检查文件类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只能上传图片文件")
    
    # 读取图片数据
    contents = await file.read()
    
    # 检查文件大小 (最大10MB)
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="图片大小不能超过10MB")
    
    try:
        # 使用PIL处理图片
        image = Image.open(io.BytesIO(contents))
        
        # 生成图片ID
        image_id = f"img_{uuid.uuid4().hex[:12]}"
        
        # 保存图片
        file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else 'jpg'
        file_path = os.path.join(UPLOAD_DIR, f"{image_id}.{file_extension}")
        
        # 保存原图
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # 存储图片信息
        IMAGE_DATA[image_id] = {
            "id": image_id,
            "path": file_path,
            "width": image.width,
            "height": image.height,
            "size": len(contents),
            "format": image.format,
            "created_at": datetime.now(),
            "original_name": file.filename
        }
        
        # 生成访问URL
        image_url = f"http://localhost:8000/api/images/{image_id}"
        
        return ImageUploadResponse(
            image_id=image_id,
            image_url=image_url,
            width=image.width,
            height=image.height,
            size=len(contents),
            format=image.format
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片处理失败: {str(e)}")

@router.get("/{image_id}")
async def get_image(image_id: str):
    """
    获取图片
    """
    image_info = IMAGE_DATA.get(image_id)
    
    if not image_info:
        raise HTTPException(status_code=404, detail="图片不存在")
    
    # 读取图片文件
    try:
        with open(image_info["path"], "rb") as f:
            image_data = f.read()
        
        # 返回图片数据
        return {
            "image_id": image_id,
            "image_data": base64.b64encode(image_data).decode(),
            "format": image_info["format"],
            "width": image_info["width"],
            "height": image_info["height"],
            "size": image_info["size"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取图片失败: {str(e)}")

@router.post("/process")
async def process_image(request: ImageProcessRequest):
    """
    处理图片
    """
    image_info = IMAGE_DATA.get(request.image_id)
    
    if not image_info:
        raise HTTPException(status_code=404, detail="图片不存在")
    
    try:
        # 读取原图
        image = Image.open(image_info["path"])
        
        # 根据操作类型处理图片
        if request.operation == "resize":
            width = request.params.get("width", image.width)
            height = request.params.get("height", image.height)
            image = image.resize((width, height), Image.Resampling.LANCZOS)
            
        elif request.operation == "crop":
            left = request.params.get("left", 0)
            top = request.params.get("top", 0)
            right = request.params.get("right", image.width)
            bottom = request.params.get("bottom", image.height)
            image = image.crop((left, top, right, bottom))
            
        elif request.operation == "rotate":
            angle = request.params.get("angle", 0)
            image = image.rotate(angle, expand=True)
            
        elif request.operation == "filter":
            filter_type = request.params.get("type", "BLUR")
            if filter_type == "BLUR":
                from PIL import ImageFilter
                image = image.filter(ImageFilter.BLUR)
            elif filter_type == "CONTOUR":
                from PIL import ImageFilter
                image = image.filter(ImageFilter.CONTOUR)
        
        # 保存处理后的图片
        processed_id = f"processed_{request.image_id}_{uuid.uuid4().hex[:8]}"
        processed_path = os.path.join(UPLOAD_DIR, f"{processed_id}.jpg")
        
        image.save(processed_path, "JPEG")
        
        # 存储处理后的图片信息
        IMAGE_DATA[processed_id] = {
            "id": processed_id,
            "path": processed_path,
            "width": image.width,
            "height": image.height,
            "size": os.path.getsize(processed_path),
            "format": "JPEG",
            "created_at": datetime.now(),
            "original_id": request.image_id
        }
        
        return {
            "processed_id": processed_id,
            "image_url": f"http://localhost:8000/api/images/{processed_id}",
            "width": image.width,
            "height": image.height,
            "format": "JPEG"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片处理失败: {str(e)}")

@router.post("/collage")
async def create_collage(request: CollageRequest):
    """
    创建图片拼接（拼贴）
    """
    if len(request.images) < 2:
        raise HTTPException(status_code=400, detail="至少需要2张图片才能创建拼贴")
    
    try:
        # 根据模板创建拼贴
        if request.template == "grid2":
            # 2宫格
            result = await create_grid_collage(request.images, 1, 2, request.spacing, request.background_color)
        elif request.template == "grid3":
            # 3宫格
            result = await create_grid_collage(request.images, 2, 2, request.spacing, request.background_color)
        elif request.template == "grid4":
            # 4宫格
            result = await create_grid_collage(request.images, 2, 2, request.spacing, request.background_color)
        elif request.template == "grid6":
            # 6宫格
            result = await create_grid_collage(request.images, 2, 3, request.spacing, request.background_color)
        elif request.template == "grid9":
            # 9宫格
            result = await create_grid_collage(request.images, 3, 3, request.spacing, request.background_color)
        else:
            raise HTTPException(status_code=400, detail="不支持的模板类型")
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建拼贴失败: {str(e)}")

async def create_grid_collage(images: List[str], rows: int, cols: int, spacing: int, background_color: str):
    """
    创建网格拼贴
    """
    # 这里简化处理，实际应该下载图片并处理
    # 返回一个模拟的拼贴结果
    collage_id = f"collage_{uuid.uuid4().hex[:12]}"
    
    return {
        "collage_id": collage_id,
        "collage_url": f"http://localhost:8000/api/images/collage/{collage_id}",
        "template": f"{rows}x{cols}",
        "image_count": len(images),
        "width": cols * 200 + (cols - 1) * spacing,
        "height": rows * 200 + (rows - 1) * spacing,
        "created_at": datetime.now()
    }

@router.get("/templates")
async def get_templates():
    """
    获取可用的图片模板
    """
    return {
        "templates": [
            {
                "id": "grid2",
                "name": "2宫格",
                "description": "2张图片拼接",
                "preview": "http://localhost:8000/static/templates/grid2.jpg"
            },
            {
                "id": "grid3",
                "name": "3宫格",
                "description": "3张图片拼接",
                "preview": "http://localhost:8000/static/templates/grid3.jpg"
            },
            {
                "id": "grid4",
                "name": "4宫格",
                "description": "4张图片拼接",
                "preview": "http://localhost:8000/static/templates/grid4.jpg"
            },
            {
                "id": "grid6",
                "name": "6宫格",
                "description": "6张图片拼接",
                "preview": "http://localhost:8000/static/templates/grid6.jpg"
            },
            {
                "id": "grid9",
                "name": "9宫格",
                "description": "9张图片拼接",
                "preview": "http://localhost:8000/static/templates/grid9.jpg"
            }
        ]
    }