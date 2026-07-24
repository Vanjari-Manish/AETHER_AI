import os
from dotenv import load_dotenv

# Load environment variables from parent .env file
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(parent_dir, ".env"))

class Settings:
    # Environment Setup
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = ENV.lower() == "development"

    # MySQL Configuration
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT", "3306")
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "gpo_auth")

    # SQLite Configuration
    SQLITE_DB_NAME: str = os.getenv("SQLITE_DB_NAME", "gpo_auth.db")
    SQLITE_PATH: str = os.path.join(parent_dir, SQLITE_DB_NAME)

    # Database Pool Settings
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "1800"))
    DB_POOL_TIMEOUT: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))

    # Security Configuration
    JWT_SECRET: str = os.getenv("JWT_SECRET", "gpo-enterprise-jwt-decisions-secret-key-2026")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: str = os.path.join(parent_dir, "logs")

settings = Settings()
