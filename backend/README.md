# QuickPush Backend

基于FastAPI的QuickPush后端服务，提供文案分享和管理功能。

## 功能特性

- 文案列表接口
- 文案详情接口  
- 分享内容生成
- 图片处理和管理
- 与微信小程序集成

## 项目结构

```
backend/
├── main.py                 # 主应用入口
├── requirements.txt        # 依赖包
├── config/                # 配置文件
├── models/                # 数据模型
├── routes/                # API路由
├── services/              # 业务逻辑
├── utils/                 # 工具函数
└── database/              # 数据库相关
```

## 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行服务：
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

## API文档

服务启动后访问：http://localhost:8001/docs