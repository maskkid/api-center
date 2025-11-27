from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, CHAR, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class Store(Base):
    __tablename__ = "1peng_store"

    store_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_name: Mapped[str | None] = mapped_column(String(80))
    address: Mapped[str | None] = mapped_column(String(255))
    contact_name: Mapped[str | None] = mapped_column(String(30))
    contact_phone: Mapped[str | None] = mapped_column(String(30))
    store_logo: Mapped[str | None] = mapped_column(String(800))  # logo图片URL
    store_banner: Mapped[str | None] = mapped_column(String(800))  # 背景图URL
    store_intro: Mapped[str | None] = mapped_column(String(800))  # 店铺介绍
    create_by: Mapped[str] = mapped_column(String(64), default="")
    create_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    update_by: Mapped[str | None] = mapped_column(String(64), default=None)
    update_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    status: Mapped[str | None] = mapped_column(CHAR(1), default="0")  # 1启用;0关闭
    ext_conf: Mapped[str] = mapped_column(String(1200), default="")

    activities: Mapped[list["Activity"]] = relationship("Activity", back_populates="store")
    resources: Mapped[list["Resource"]] = relationship("Resource", back_populates="store")


class Activity(Base):
    __tablename__ = "1peng_activity"

    activity_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("1peng_store.store_id"), nullable=False)
    create_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    create_by: Mapped[str | None] = mapped_column(String(64), default=None)
    update_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    update_by: Mapped[str | None] = mapped_column(String(64), default=None)
    status: Mapped[str | None] = mapped_column(CHAR(1), default="0")  # 1启用;0关闭
    ext_conf: Mapped[str | None] = mapped_column(String(2000))  # JSON custom config

    store: Mapped["Store"] = relationship("Store", back_populates="activities")
    resources: Mapped[list["ActivityResource"]] = relationship(
        "ActivityResource", back_populates="activity", cascade="all, delete-orphan"
    )


class Resource(Base):
    __tablename__ = "1peng_res"

    res_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    res_platform: Mapped[str | None] = mapped_column(String(20))  # xhs;douyin;dazhong;meituan
    text: Mapped[str | None] = mapped_column(String(800))
    video: Mapped[str | None] = mapped_column(String(800))
    image: Mapped[str | None] = mapped_column(String(2000))  # comma-separated
    del_flag: Mapped[str | None] = mapped_column(CHAR(1), default="0")  # 0正常;2删除
    store_id: Mapped[int] = mapped_column(ForeignKey("1peng_store.store_id"), nullable=False)
    create_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    create_by: Mapped[str | None] = mapped_column(String(64), default=None)
    update_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    update_by: Mapped[str | None] = mapped_column(String(64), default=None)

    store: Mapped["Store"] = relationship("Store", back_populates="resources")
    activities: Mapped[list["ActivityResource"]] = relationship(
        "ActivityResource", back_populates="resource", cascade="all, delete-orphan"
    )


class ActivityResource(Base):
    __tablename__ = "1peng_activity_res"

    res_id: Mapped[int] = mapped_column(ForeignKey("1peng_res.res_id"), primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("1peng_activity.activity_id"), primary_key=True)
    user_num: Mapped[int] = mapped_column(Integer, default=0)

    activity: Mapped["Activity"] = relationship("Activity", back_populates="resources")
    resource: Mapped["Resource"] = relationship("Resource", back_populates="activities")


class Share(Base):
    __tablename__ = "1peng_share"

    share_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    share_code: Mapped[str | None] = mapped_column(String(80), unique=True)
    res_id: Mapped[int] = mapped_column(ForeignKey("1peng_res.res_id"), nullable=False)
    status: Mapped[str | None] = mapped_column(CHAR(1), default="0")  # 0 开启, 1 关闭
    share_num: Mapped[int] = mapped_column(Integer, default=0)
    download_num: Mapped[int] = mapped_column(Integer, default=0)
    share_channel: Mapped[str | None] = mapped_column(String(2000), default=None)
    create_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    create_by: Mapped[str | None] = mapped_column(String(255), default=None)

    resource: Mapped["Resource"] = relationship("Resource", primaryjoin="Share.res_id==Resource.res_id")


class ShareLog(Base):
    __tablename__ = "1peng_share_log"

    log_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    share_id: Mapped[int] = mapped_column(Integer, nullable=False)
    share_channel: Mapped[str | None] = mapped_column(String(255), default=None)
    res_id: Mapped[int] = mapped_column(Integer, nullable=False)
    create_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    ip: Mapped[str | None] = mapped_column(String(60), default=None)