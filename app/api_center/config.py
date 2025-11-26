import os
import yaml


class Config:
    """Application configuration. Values come from environment variables
    and can be overridden by a top-level `config.yml` file.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key')

    # MySQL配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123456')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'api_platform')

    # API费用配置
    POINT_RATE = 100  # 1元 = 100积分
    API_COSTS = {
        'chat': 1,    # 基础聊天消耗1积分
        'genimg': 5,  # 生成图片消耗5积分
        'tts': 2,     # 语音合成消耗2积分
        'asr': 2,     # 语音识别消耗2积分
        'ocr': 2      # 文字识别消耗2积分
    }

    # Application
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = False


def load_yaml_config(path=None):
    """Load YAML config and override attributes on Config.

    If `path` is None the function looks for `config.yml` at the repository root.
    """
    if path is None:
        # guess repository root relative to this file (three levels up to get to project root)
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        path = os.path.join(base, 'config.yml')

    if not os.path.exists(path):
        return

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
    except Exception:
        return

    # override attributes if present in yaml
    for key, val in data.items():
        if hasattr(Config, key):
            setattr(Config, key, val)
        else:
            # set new attributes as well
            setattr(Config, key, val)


# Attempt to load config.yml at import time (non-fatal)
try:
    load_yaml_config()
except Exception:
    pass
