from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
import models
import schemas

router = APIRouter(prefix="/resources", tags=["resources"])

@router.get("", response_model=dict)
def list_resources(
    store_id: Optional[int] = Query(None, description="店铺ID"),
    res_platform: Optional[str] = Query(None, description="平台类型"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
):
    """
    获取资源列表（用于小程序首页文案列表）
    """
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10
    
    # 查询资源，排除已删除的
    q = db.query(models.Resource).filter(models.Resource.del_flag != "2")
    
    if store_id is not None:
        q = q.filter(models.Resource.store_id == store_id)
    
    if res_platform is not None:
        q = q.filter(models.Resource.res_platform == res_platform)
    
    # 按创建时间倒序排列
    q = q.order_by(models.Resource.create_at.desc())
    
    total = q.count()
    offset = max(page - 1, 0) * page_size
    resources = q.offset(offset).limit(page_size).all()
    
    if not resources:
        return {
            "items": [], 
            "total": total, 
            "page": page, 
            "page_size": page_size
        }
    
    # 获取关联的分享信息
    res_ids = [r.res_id for r in resources]
    shares = {
        s.res_id: s
        for s in db.query(models.Share)
        .filter(models.Share.res_id.in_(res_ids))
        .all()
    }
    
    result = []
    for resource in resources:
        share = shares.get(resource.res_id)
        item = {
            "resource": schemas.ResourceOut.model_validate(resource),
        }
        
        if share:
            item["share"] = schemas.ShareOut.model_validate(share)
        else:
            item["share"] = None
            
        result.append(item)
    
    return {
        "items": result, 
        "total": total, 
        "page": page, 
        "page_size": page_size
    }


@router.get("/{res_id}", response_model=schemas.ResourceOut)
def get_resource(
    res_id: int,
    db: Session = Depends(get_db),
):
    """
    获取单个资源详情
    """
    resource = db.get(models.Resource, res_id)
    if not resource or resource.del_flag == "2":
        raise HTTPException(status_code=404, detail="资源不存在或已删除")
    
    return schemas.ResourceOut.model_validate(resource)