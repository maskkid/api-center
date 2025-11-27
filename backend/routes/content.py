from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class ContentItem(BaseModel):
    id: int
    title: str
    content: str
    images: List[str]
    category: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    author: str
    likes: int
    views: int

class ContentListResponse(BaseModel):
    items: List[ContentItem]
    total: int
    page: int
    page_size: int
    has_next: bool

class ContentDetailResponse(BaseModel):
    item: ContentItem
    related_items: List[ContentItem]

# 模拟数据 - 文案列表
MOCK_CONTENTS = [
    {
        "id": 1,
        "title": "早安励志文案",
        "content": "每一个清晨，都是新的开始。不管昨天发生了什么，今天都是崭新的一天。愿你带着希望和勇气，迎接每一个挑战。早安，世界！",
        "images": [
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
            "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=400"
        ],
        "category": "励志",
        "tags": ["早安", "励志", "正能量"],
        "created_at": "2024-01-15T08:00:00",
        "updated_at": "2024-01-15T08:00:00",
        "author": "文案小助手",
        "likes": 128,
        "views": 1024
    },
    {
        "id": 2,
        "title": "朋友圈治愈文案",
        "content": "生活就像一杯茶，不会苦一辈子，但总会苦一阵子。愿你在苦涩中品味甘甜，在平凡中发现美好。",
        "images": [
            "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400",
            "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400"
        ],
        "category": "治愈",
        "tags": ["朋友圈", "治愈", "温暖"],
        "created_at": "2024-01-14T15:30:00",
        "updated_at": "2024-01-14T15:30:00",
        "author": "文案小助手",
        "likes": 95,
        "views": 856
    },
    {
        "id": 3,
        "title": "工作励志文案",
        "content": "成功不是一蹴而就的，而是每天一点一滴的积累。今天的努力，是为了明天的收获。加油，打工人！",
        "images": [
            "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400"
        ],
        "category": "励志",
        "tags": ["工作", "励志", "奋斗"],
        "created_at": "2024-01-13T09:15:00",
        "updated_at": "2024-01-13T09:15:00",
        "author": "文案小助手",
        "likes": 76,
        "views": 642
    },
    {
        "id": 4,
        "title": "爱情甜蜜文案",
        "content": "最好的爱情，是两个人一起变得更好。不是互相拖累，而是相互成就。愿你我都能在爱里成为更好的自己。",
        "images": [
            "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=400",
            "https://images.unsplash.com/photo-1494790108755-2616b612b5bc?w=400"
        ],
        "category": "爱情",
        "tags": ["爱情", "甜蜜", "浪漫"],
        "created_at": "2024-01-12T20:00:00",
        "updated_at": "2024-01-12T20:00:00",
        "author": "文案小助手",
        "likes": 156,
        "views": 1280
    },
    {
        "id": 5,
        "title": "生活感悟文案",
        "content": "人生就像一场旅行，不必在乎目的地，在乎的是沿途的风景以及看风景的心情。珍惜当下，享受过程。",
        "images": [
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"
        ],
        "category": "感悟",
        "tags": ["生活", "感悟", "哲理"],
        "created_at": "2024-01-11T16:45:00",
        "updated_at": "2024-01-11T16:45:00",
        "author": "文案小助手",
        "likes": 89,
        "views": 734
    }
]

@router.get("/list", response_model=ContentListResponse)
async def get_content_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    category: Optional[str] = Query(None, description="分类筛选"),
    search: Optional[str] = Query(None, description="搜索关键词")
):
    """
    获取文案列表
    """
    # 过滤数据
    filtered_contents = MOCK_CONTENTS
    
    if category:
        filtered_contents = [item for item in filtered_contents if item["category"] == category]
    
    if search:
        filtered_contents = [
            item for item in filtered_contents 
            if search.lower() in item["title"].lower() or search.lower() in item["content"].lower()
        ]
    
    # 分页
    total = len(filtered_contents)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    items = filtered_contents[start_idx:end_idx]
    
    # 转换为响应模型
    content_items = []
    for item in items:
        content_item = ContentItem(
            id=item["id"],
            title=item["title"],
            content=item["content"],
            images=item["images"],
            category=item["category"],
            tags=item["tags"],
            created_at=datetime.fromisoformat(item["created_at"]),
            updated_at=datetime.fromisoformat(item["updated_at"]),
            author=item["author"],
            likes=item["likes"],
            views=item["views"]
        )
        content_items.append(content_item)
    
    return ContentListResponse(
        items=content_items,
        total=total,
        page=page,
        page_size=page_size,
        has_next=end_idx < total
    )

@router.get("/{content_id}", response_model=ContentDetailResponse)
async def get_content_detail(content_id: int):
    """
    获取文案详情
    """
    content_item = next((item for item in MOCK_CONTENTS if item["id"] == content_id), None)
    
    if not content_item:
        raise HTTPException(status_code=404, detail="文案不存在")
    
    # 获取相关文案（同分类的其他文案）
    related_items = [
        item for item in MOCK_CONTENTS 
        if item["category"] == content_item["category"] and item["id"] != content_id
    ][:3]  # 只取前3个
    
    # 转换为响应模型
    main_item = ContentItem(
        id=content_item["id"],
        title=content_item["title"],
        content=content_item["content"],
        images=content_item["images"],
        category=content_item["category"],
        tags=content_item["tags"],
        created_at=datetime.fromisoformat(content_item["created_at"]),
        updated_at=datetime.fromisoformat(content_item["updated_at"]),
        author=content_item["author"],
        likes=content_item["likes"],
        views=content_item["views"]
    )
    
    related_content_items = []
    for item in related_items:
        related_item = ContentItem(
            id=item["id"],
            title=item["title"],
            content=item["content"],
            images=item["images"],
            category=item["category"],
            tags=item["tags"],
            created_at=datetime.fromisoformat(item["created_at"]),
            updated_at=datetime.fromisoformat(item["updated_at"]),
            author=item["author"],
            likes=item["likes"],
            views=item["views"]
        )
        related_content_items.append(related_item)
    
    return ContentDetailResponse(
        item=main_item,
        related_items=related_content_items
    )

@router.post("/{content_id}/like")
async def like_content(content_id: int):
    """
    点赞文案
    """
    content_item = next((item for item in MOCK_CONTENTS if item["id"] == content_id), None)
    
    if not content_item:
        raise HTTPException(status_code=404, detail="文案不存在")
    
    # 模拟点赞操作
    content_item["likes"] += 1
    
    return {"message": "点赞成功", "likes": content_item["likes"]}

@router.post("/{content_id}/view")
async def view_content(content_id: int):
    """
    增加浏览量
    """
    content_item = next((item for item in MOCK_CONTENTS if item["id"] == content_id), None)
    
    if not content_item:
        raise HTTPException(status_code=404, detail="文案不存在")
    
    # 模拟浏览操作
    content_item["views"] += 1
    
    return {"message": "浏览记录已更新", "views": content_item["views"]}