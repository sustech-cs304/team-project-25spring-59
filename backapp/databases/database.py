from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

"""
数据库连接配置
"""
# SQLite数据库路径设置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_DB_PATH = os.path.join(BASE_DIR, "sqlite_health_assistant.db")

# 构建SQLite数据库URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"

# 原始MySQL连接字符串（保留作为参考）
# DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
# DB_USER = os.environ.get("DB_USER", "root")
# DB_PASSWORD = os.environ.get("DB_PASSWORD", "123456")
# DB_NAME = os.environ.get("DB_NAME", "health_assistant")
# SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

# 创建同步引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # SQLite特定设置
    connect_args={"check_same_thread": False}  # 允许多线程访问
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 获取数据库会话的依赖函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()