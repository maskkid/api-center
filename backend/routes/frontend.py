from fastapi import APIRouter, HTTPException, Query, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from config import config
import json

router = APIRouter(tags=["frontend"])

@router.get("/res/share/{share_code}", response_class=HTMLResponse)
def frontend_share_page(
    share_code: str,
    channel: str = Query(None, description="渠道标识"),
    db: Session = Depends(get_db),
):
    """
    前端分享页面，模拟 quickpush 的 /res/share 接口
    用于网页端跳转到小程序页面
    """
    # 获取分享信息
    share = db.query(models.Share).filter(models.Share.share_code == share_code).first()
    if not share:
        raise HTTPException(status_code=404, detail="分享不存在")
    
    if share.status == "1":
        raise HTTPException(status_code=403, detail="分享已关闭")
    
    # 获取资源信息
    resource = db.get(models.Resource, share.res_id)
    if not resource or resource.del_flag == "2":
        raise HTTPException(status_code=404, detail="资源不存在或已删除")
    
    # 处理图片列表
    image_list = []
    if resource.image:
        image_list = [img.strip() for img in resource.image.split(",") if img.strip()]
    
    # 构建小程序跳转参数
    encoded_content = resource.text.replace("\n", "%20").replace(" ", "%20") if resource.text else ""
    encoded_images = ",".join(image_list)
    
    # 构建小程序路径
    miniprogram_path = f"/pages/modules/wenan/detail?content={encoded_content}&images={encoded_images}"
    
    # 构建图片HTML
    image_html = ""
    if image_list:
        image_items = []
        for i, img in enumerate(image_list):
            image_items.append(f'<img src="{img}" class="image-item" alt="图片{i+1}" onclick="window.open(\'{img}\', \'_blank\')">')
        image_html = '<div class="content-section"><div class="section-title">图片素材</div><div class="image-grid">' + ''.join(image_items) + '</div></div>'
    
    # 构建文案HTML
    text_html = ""
    if resource.text:
        text_html = f'<div class="content-section"><div class="section-title">文案内容</div><div class="text-content">{resource.text}</div></div>'
    
    # 返回 HTML 页面
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>分享内容</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f6f7;
            line-height: 1.6;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 24px;
        }}
        .title {{
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }}
        .share-code {{
            font-size: 14px;
            color: #666;
        }}
        .content-section {{
            margin-bottom: 24px;
        }}
        .section-title {{
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 12px;
        }}
        .text-content {{
            background: #f8f9fa;
            padding: 16px;
            border-radius: 8px;
            font-size: 14px;
            color: #333;
            white-space: pre-wrap;
        }}
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 12px;
            margin-bottom: 24px;
        }}
        .image-item {{
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 8px;
            cursor: pointer;
        }}
        .action-buttons {{
            display: flex;
            gap: 12px;
            justify-content: center;
        }}
        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-primary {{
            background: #07c160;
            color: white;
        }}
        .btn-primary:hover {{
            background: #06a050;
        }}
        .btn-secondary {{
            background: #f0f0f0;
            color: #333;
        }}
        .btn-secondary:hover {{
            background: #e0e0e0;
        }}
        .tips {{
            background: #fff1b8;
            color: #874d00;
            padding: 12px;
            border-radius: 8px;
            font-size: 13px;
            margin-bottom: 16px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">分享内容</div>
            <div class="share-code">分享码：{share_code}</div>
        </div>
        
        <div class="tips">
            💡 提示：点击下方按钮可以在小程序中查看完整内容
        </div>
        
        {text_html}
        {image_html}
        
        <div class="action-buttons">
            <button class="btn btn-primary" onclick="openMiniprogram()">在小程序中打开</button>
            <button class="btn btn-secondary" onclick="copyContent()">复制文案</button>
        </div>
    </div>
    
    <script>
        function openMiniprogram() {{
            // 尝试打开小程序
            if (typeof wx !== 'undefined' && wx.miniProgram) {{
                wx.miniProgram.navigateTo({{
                    url: '{miniprogram_path}'
                }});
            }} else {{
                // 如果不是在微信环境中，显示提示
                alert('请在微信中打开此页面，或手动复制以下路径到小程序：\\n\\n{miniprogram_path}');
            }}
        }}
        
        function copyContent() {{
            const text = `{resource.text or ''}`;
            if (!text) {{
                alert('没有文案内容');
                return;
            }}
            
            if (navigator.clipboard) {{
                navigator.clipboard.writeText(text).then(() => {{
                    alert('文案已复制到剪贴板');
                }}).catch(() => {{
                    fallbackCopy(text);
                }});
            }} else {{
                fallbackCopy(text);
            }}
        }}
        
        function fallbackCopy(text) {{
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            textarea.style.left = '-9999px';
            document.body.appendChild(textarea);
            textarea.focus();
            textarea.select();
            try {{
                document.execCommand('copy');
                alert('文案已复制到剪贴板');
            }} catch (err) {{
                alert('复制失败，请手动选择并复制');
            }}
            document.body.removeChild(textarea);
        }}
        
        // 记录分享访问
        fetch('/api/shares/code/' + '{share_code}', {{
            method: 'GET',
            headers: {{'Content-Type': 'application/json'}},
        }});
    </script>
</body>
</html>
    """
    
    return HTMLResponse(content=html_content)