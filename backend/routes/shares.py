import json
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from config import config

router = APIRouter(prefix="/shares", tags=["shares"])

SHARE_CHANNELS = [
    {"key": "meituan", "label": "美团"},
    {"key": "dazhong", "label": "大众点评"},
    {"key": "douyin", "label": "抖音"},
    {"key": "baidu", "label": "百度地图"},
    {"key": "gaode", "label": "高德地图"},
]
CHANNEL_KEYS = [c["key"] for c in SHARE_CHANNELS]
CHANNEL_LABEL_MAP = {c["key"]: c["label"] for c in SHARE_CHANNELS}


def _generate_share_code(db: Session) -> str:
    while True:
        code = uuid.uuid4().hex[:8]
        exists = db.query(models.Share).filter(models.Share.share_code == code).first()
        if not exists:
            return code


def _default_channel_stats():
    return {key: {"share_num": 0, "download_num": 0} for key in CHANNEL_KEYS}


def _load_channel_stats(share: models.Share):
    raw = share.share_channel
    stats = _default_channel_stats()
    if not raw:
        return stats
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            for key in stats.keys():
                if key in data and isinstance(data[key], dict):
                    stats[key]["share_num"] = int(data[key].get("share_num", stats[key]["share_num"]))
                    stats[key]["download_num"] = int(data[key].get("download_num", stats[key]["download_num"]))
            return stats
    except json.JSONDecodeError:
        # fallback for comma-separated legacy data
        pass
    # legacy string like "meituan,dazhong,..."
    return stats


def _save_channel_stats(share: models.Share, stats: dict):
    share.share_channel = json.dumps(stats, ensure_ascii=False)


def _get_channel_label(key: str) -> str:
    return CHANNEL_LABEL_MAP.get(key, key)


def _build_channel_url(share_code: str, channel_key: str) -> str:
    return f"/res/share/{share_code}?channel={channel_key}"


def _build_channel_info(share: models.Share, channel_key: str, stats: dict) -> dict:
    channel_stats = stats.get(channel_key, {"share_num": 0, "download_num": 0})
    return {
        "channel": channel_key,
        "label": _get_channel_label(channel_key),
        "share_num": channel_stats.get("share_num", 0),
        "download_num": channel_stats.get("download_num", 0),
        "url": _build_channel_url(share.share_code, channel_key),
        "download_limit": config.share_download_limit,
    }


def _build_channels_response(share: models.Share, stats: dict):
    return [
        _build_channel_info(share, key, stats)
        for key in CHANNEL_KEYS
    ]


@router.get("", response_model=schemas.ShareListResponse)
def list_shares(
    store_id: int | None = None,
    status: str | None = None,
    sort_by: str = "download_num",
    sort_order: str = "asc",
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
):
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10
    q = db.query(models.Share).join(models.Resource)
    if status is not None:
        q = q.filter(models.Share.status == status)
    if store_id is not None:
        q = q.filter(models.Resource.store_id == store_id)
    sort_column = models.Share.download_num if sort_by not in {"share_num", "download_num"} else getattr(models.Share, sort_by)
    if sort_order == "desc":
        q = q.order_by(sort_column.desc())
    else:
        q = q.order_by(sort_column.asc())
    total = q.count()
    offset = max(page - 1, 0) * page_size
    shares = q.offset(offset).limit(page_size).all()
    if not shares:
        return {"items": [], "total": total, "page": page, "page_size": page_size}
    res_ids = [s.res_id for s in shares]
    resources = {
        r.res_id: r
        for r in db.query(models.Resource)
        .filter(models.Resource.res_id.in_(res_ids))
        .all()
    }
    result = []
    for s in shares:
        res = resources.get(s.res_id)
        if not res:
            continue
        stats = _load_channel_stats(s)
        result.append(
            {
                "share": schemas.ShareOut.model_validate(s),
                "resource": schemas.ResourceOut.model_validate(res),
                "channels": _build_channels_response(s, stats),
            }
        )
    return {"items": result, "total": total, "page": page, "page_size": page_size}


@router.post("", response_model=schemas.ShareOut)
def create_share(payload: schemas.ShareCreate, db: Session = Depends(get_db)):
    # Validate resource exists
    resource = db.get(models.Resource, payload.res_id)
    if not resource:
        raise HTTPException(status_code=400, detail="资源不存在")

    share_code = payload.share_code or _generate_share_code(db)
    # Ensure unique
    exists = db.query(models.Share).filter(models.Share.share_code == share_code).first()
    if exists:
        raise HTTPException(status_code=400, detail="分享码已存在")

    share = models.Share(
        share_code=share_code,
        res_id=payload.res_id,
        status=payload.status or "0",
        share_num=0,
        download_num=0,
        create_at=datetime.now(),
        create_by=payload.create_by or "admin",
    )
    _save_channel_stats(share, _default_channel_stats())
    db.add(share)
    db.commit()
    db.refresh(share)
    return share


def _get_share_by_code(share_code: str, db: Session, include_disabled: bool = False) -> models.Share:
    share = db.query(models.Share).filter(models.Share.share_code == share_code).first()
    if not share:
        raise HTTPException(status_code=404, detail="分享不存在")
    if share.status == "1" and not include_disabled:
        raise HTTPException(status_code=403, detail="分享已关闭")
    return share


@router.get("/code/{share_code}", response_model=schemas.ShareDetail)
def get_share_detail(
    share_code: str,
    request: Request,
    channel: str | None = Query(None, description="渠道标识"),
    db: Session = Depends(get_db),
):
    share = _get_share_by_code(share_code, db, include_disabled=True)
    resource = db.get(models.Resource, share.res_id)
    if not resource or resource.del_flag == "2":
        raise HTTPException(status_code=404, detail="资源不存在或已删除")

    channel_key = channel if channel in CHANNEL_KEYS else CHANNEL_KEYS[0]
    stats = _load_channel_stats(share)
    disabled = share.status == "1"

    if not disabled:
        stats[channel_key]["share_num"] = stats[channel_key].get("share_num", 0) + 1
        share.share_num = (share.share_num or 0) + 1
        _save_channel_stats(share, stats)
        db.add(share)
        db.add(
            models.ShareLog(
                share_id=share.share_id,
                res_id=share.res_id,
                share_channel=channel_key,
                create_at=datetime.now(),
                ip=request.client.host if request.client else None,
            )
        )
        db.commit()

    return {
        "share": schemas.ShareOut.model_validate(share),
        "resource": schemas.ResourceOut.model_validate(resource),
        "disabled": disabled,
        "channel": _build_channel_info(share, channel_key, stats),
    }


@router.post("/code/{share_code}/download")
def download_share(
    share_code: str,
    channel: str | None = Query(None, description="渠道标识"),
    request: Request = None,
    db: Session = Depends(get_db),
):
    share = _get_share_by_code(share_code, db)
    if share.status == "1":
        raise HTTPException(status_code=400, detail="分享已关闭")
    channel_key = channel if channel in CHANNEL_KEYS else CHANNEL_KEYS[0]
    stats = _load_channel_stats(share)
    limit = config.share_download_limit
    current_download = stats[channel_key].get("download_num", 0)
    if limit > 0 and current_download >= limit:
        raise HTTPException(status_code=400, detail="已经被分享过了，请勿重复下载")
    stats[channel_key]["download_num"] = current_download + 1
    share.download_num = (share.download_num or 0) + 1
    _save_channel_stats(share, stats)
    db.add(share)
    db.add(
        models.ShareLog(
            share_id=share.share_id,
            res_id=share.res_id,
            share_channel=channel_key,
            create_at=datetime.now(),
            ip=request.client.host if request and request.client else None,
        )
    )
    db.commit()
    return {
        "ok": True,
        "share_code": share_code,
        "channel": channel_key,
        "download_num": stats[channel_key]["download_num"],
    }


@router.patch("/{share_id}/status", response_model=schemas.ShareOut)
def update_share_status(share_id: int, payload: schemas.ShareUpdate, db: Session = Depends(get_db)):
    share = db.get(models.Share, share_id)
    if not share:
        raise HTTPException(status_code=404, detail="分享不存在")
    if payload.status not in {"0", "1"}:
        raise HTTPException(status_code=400, detail="状态值不合法")
    share.status = payload.status
    db.add(share)
    db.commit()
    db.refresh(share)
    return share