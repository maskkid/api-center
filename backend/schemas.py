from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class StoreBase(BaseModel):
    store_name: Optional[str] = None
    address: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    store_logo: Optional[str] = None
    store_banner: Optional[str] = None
    store_intro: Optional[str] = None
    status: Optional[str] = "0"


class StoreCreate(StoreBase):
    pass


class StoreUpdate(StoreBase):
    pass


class StoreOut(StoreBase):
    model_config = ConfigDict(from_attributes=True)
    store_id: int
    create_at: Optional[datetime] = None
    create_by: Optional[str] = None
    update_at: Optional[datetime] = None
    update_by: Optional[str] = None
    ext_conf: Optional[str] = None


class ActivityBase(BaseModel):
    store_id: int
    status: Optional[str] = "0"
    ext_conf: Optional[str] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    status: Optional[str] = None
    ext_conf: Optional[str] = None


class ActivityOut(ActivityBase):
    model_config = ConfigDict(from_attributes=True)
    activity_id: int
    create_at: Optional[datetime] = None
    create_by: Optional[str] = None
    update_at: Optional[datetime] = None
    update_by: Optional[str] = None


class ResourceBase(BaseModel):
    res_platform: Optional[str] = None
    text: Optional[str] = None
    video: Optional[str] = None
    image: Optional[str] = None
    store_id: int
    del_flag: Optional[str] = "0"


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    res_platform: Optional[str] = None
    text: Optional[str] = None
    video: Optional[str] = None
    image: Optional[str] = None
    del_flag: Optional[str] = None


class ResourceOut(ResourceBase):
    model_config = ConfigDict(from_attributes=True)
    res_id: int
    create_at: Optional[datetime] = None
    create_by: Optional[str] = None
    update_at: Optional[datetime] = None
    update_by: Optional[str] = None


class ShareBase(BaseModel):
    share_code: Optional[str] = None
    res_id: int
    status: Optional[str] = "0"
    share_num: Optional[int] = 0
    download_num: Optional[int] = 0
    share_channel: Optional[str] = None


class ShareCreate(ShareBase):
    pass


class ShareUpdate(BaseModel):
    status: Optional[str] = None


class ShareOut(ShareBase):
    model_config = ConfigDict(from_attributes=True)
    share_id: int
    create_at: Optional[datetime] = None
    create_by: Optional[str] = None


class ShareListResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    page_size: int


class ShareDetail(BaseModel):
    share: ShareOut
    resource: ResourceOut
    disabled: bool
    channel: Optional[dict] = None


class ShareChannelInfo(BaseModel):
    channel: str
    label: str
    share_num: int
    download_num: int
    url: str
    download_limit: int