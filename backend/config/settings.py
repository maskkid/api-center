import os
from dataclasses import dataclass, field

@dataclass(frozen=True)
class AppConfig:
    # MySQL 配置
    mysql_user: str = os.getenv("MYSQL_USER", "root")
    mysql_password: str = os.getenv("MYSQL_PASSWORD", "must_change_password")
    mysql_host: str = os.getenv("MYSQL_HOST", "192.168.1.24")
    mysql_port: str = os.getenv("MYSQL_PORT", "3306")
    mysql_db: str = os.getenv("MYSQL_DB", "24_quickpush")
    sql_echo: bool = os.getenv("SQL_ECHO", "0") == "1"

    # 管理员配置
    admin_token: str = os.getenv("ADMIN_TOKEN", "quickpush-admin-token")
    admin_username: str = os.getenv("ADMIN_USERNAME", "admin")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "admin123")
    share_download_limit: int = int(os.getenv("SHARE_DOWNLOAD_LIMIT", "1"))

    # API 配置
    api_title: str = os.getenv("API_TITLE", "QuickPush API")
    api_version: str = os.getenv("API_VERSION", "0.1.0")

    # 服务器配置
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    cors_origins: list[str] = field(default_factory=lambda: os.getenv("CORS_ORIGINS", "*").split(","))

    @property
    def database_url(self) -> str:
        # Use PyMySQL driver to avoid MySQLdb issues on Python 3.12/macOS
        return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"

config = AppConfig()