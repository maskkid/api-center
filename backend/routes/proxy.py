from fastapi import APIRouter, HTTPException, Query, Response
import httpx
import asyncio
from typing import Optional

router = APIRouter()

@router.get("/proxy")
async def proxy_url(
    url: str = Query(..., description="要代理的URL")
):
    """
    代理转发接口 - 将跨域资源路径转换到当前域下
    用于解决小程序中无法直接访问外部图片的问题
    返回原始的二进制数据
    """
    if not url:
        raise HTTPException(status_code=400, detail="URL参数不能为空")
    
    try:
        # 创建HTTP客户端
        async with httpx.AsyncClient() as client:
            # 发送GET请求获取资源，允许重定向
            response = await client.get(url, timeout=30.0, follow_redirects=True)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"无法获取资源: {response.status_code}"
                )
            
            # 获取内容类型
            content_type = response.headers.get('content-type', 'application/octet-stream')
            
            # 直接返回二进制响应数据
            return Response(
                content=response.content,
                media_type=content_type,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Cache-Control": "public, max-age=3600"
                }
            )
    
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"网络请求失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"代理转发失败: {str(e)}")

@router.get("/image")
async def proxy_image(
    url: str = Query(..., description="要代理的图片URL"),
    response_type: str = Query("base64", description="返回类型: base64 或 binary", regex="^(base64|binary)$")
):
    """
    图片代理转发接口 - 专门用于图片资源的代理
    支持返回base64编码数据或直接返回二进制流
    """
    if not url:
        raise HTTPException(status_code=400, detail="URL参数不能为空")
    
    try:
        # 创建HTTP客户端
        async with httpx.AsyncClient() as client:
            # 发送GET请求获取图片，允许重定向
            response = await client.get(url, timeout=30.0, follow_redirects=True)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"无法获取图片: {response.status_code}"
                )
            
            # 获取内容类型
            content_type = response.headers.get('content-type', 'image/jpeg')
            
            # 检查是否为图片类型
            if not content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="URL不是有效的图片资源")
            
            # 根据返回类型决定响应格式
            if response_type == "binary":
                # 返回二进制流数据
                return Response(
                    content=response.content,
                    media_type=content_type,
                    headers={
                        "Access-Control-Allow-Origin": "*",
                        "Cache-Control": "public, max-age=3600",
                        "Content-Disposition": f"inline; filename*=UTF-8''image.{content_type.split('/')[-1]}"
                    }
                )
            else:
                # 返回base64编码的图片数据（默认）
                import base64
                image_base64 = base64.b64encode(response.content).decode('utf-8')
                
                return {
                    "data": f"data:{content_type};base64,{image_base64}",
                    "content_type": content_type,
                    "size": len(response.content),
                    "url": url,
                    "response_type": "base64"
                }
    
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"网络请求失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片代理失败: {str(e)}")