# 工具箱后端
## 概述
新建backend目录，使用fastapi开发，数据库使用mysql，配置 192.168.1.24:3306 root must_change_password，数据库 24_quickpush。
## 功能模块
主要接口模块是文案模块，需要列表接口、点击一键下载，支持对对应平台的下载量计数的功能，提供给frontend-miniprogram小程序中的文案功能。
列表接口，只返回文案内容和图片列表，供小程序端渲染。


## 数据库

### 数据库：24_quickpush

### 表结构说明

#### 1. 1peng_store (店铺表)
| 字段 | 类型 | 说明 |
|------|------|------|
| store_id | int(10) unsigned | 主键，店铺ID |
| store_name | varchar(80) | 店铺名称 |
| address | varchar(255) | 地址 |
| contact_name | varchar(30) | 联系人 |
| contact_phone | varchar(30) | 联系电话 |
| store_logo | varchar(800) | 店铺Logo图片URL |
| store_banner | varchar(800) | 店铺背景图URL |
| store_intro | varchar(800) | 店铺介绍 |
| create_by | varchar(64) | 创建人 |
| create_at | datetime | 创建时间 |
| update_by | varchar(64) | 更新人 |
| update_at | datetime | 更新时间 |
| status | char(1) | 状态：1开启，0关闭 |
| ext_conf | varchar(1200) | 额外配置（JSON字符串） |

**索引**：PRIMARY KEY (store_id)

#### 2. 1peng_res (资源表)
| 字段 | 类型 | 说明 |
|------|------|------|
| res_id | int(10) unsigned | 主键，资源ID |
| res_platform | varchar(20) | 平台：douyin/xhs/dazhong/meituan |
| text | varchar(800) | 文字内容 |
| video | varchar(800) | 视频URL |
| image | varchar(2000) | 图片URL（多个用逗号分隔） |
| del_flag | char(1) | 删除标志：0正常，2删除 |
| store_id | int(10) unsigned | 店铺ID（外键） |
| create_at | datetime | 创建时间 |
| create_by | varchar(64) | 创建人 |
| update_at | datetime | 更新时间 |
| update_by | varchar(64) | 更新人 |

**索引**：PRIMARY KEY (res_id, store_id)

#### 3. 1peng_activity (活动表)
| 字段 | 类型 | 说明 |
|------|------|------|
| activity_id | int(10) unsigned | 主键，活动ID |
| store_id | int(10) unsigned | 店铺ID（外键） |
| create_at | datetime | 创建时间 |
| create_by | varchar(64) | 创建人 |
| update_at | datetime | 更新时间 |
| update_by | varchar(64) | 更新人 |
| status | char(1) | 状态：1开启，0关闭 |
| ext_conf | varchar(2000) | 扩展配置（JSON字符串） |

**索引**：PRIMARY KEY (activity_id, store_id)

#### 4. 1peng_activity_res (活动资源关联表)
| 字段 | 类型 | 说明 |
|------|------|------|
| res_id | int(11) | 资源ID（外键） |
| activity_id | int(11) | 活动ID（外键） |
| user_num | int(10) unsigned | 使用次数 |

**索引**：PRIMARY KEY (res_id, activity_id)

#### 5. 1peng_share (分享表)
| 字段 | 类型 | 说明 |
|------|------|------|
| share_id | int(10) unsigned | 主键，分享ID |
| share_code | varchar(80) | 分享码（唯一） |
| res_id | int(11) | 资源ID（外键） |
| status | char(1) | 状态：0开启，1关闭 |
| share_num | int(11) | 访问次数 |
| download_num | int(11) | 下载次数 |
| create_at | datetime | 创建时间 |
| create_by | varchar(255) | 创建人 |

**索引**：PRIMARY KEY (share_id, res_id)

#### 6. 1peng_share_log (分享日志表)
| 字段 | 类型 | 说明 |
|------|------|------|
| log_id | int(10) unsigned | 主键，日志ID |
| share_id | int(11) | 分享ID（外键） |
| res_id | int(11) | 资源ID（外键） |
| create_at | datetime | 访问时间 |
| ip | varchar(60) | IP地址 |

**索引**：PRIMARY KEY (log_id, share_id, res_id)

### 关系说明

1. **店铺 → 活动**：一对多关系
2. **店铺 → 资源**：一对多关系
3. **活动 ↔ 资源**：多对多关系（通过 `1peng_activity_res` 表）
4. **资源 → 分享**：一对多关系（一个资源可以有多个分享）