from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
AI-generated-content 
tool: ChatGPT 
version: 4o
usage: I used the prompt "pymysql如何连接mysql数据库，设定账号和密码”", and 
directly copy the code from its response 
"""
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:shiyansong123@localhost:3306/health_assistant"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/health_assistant"

# 创建同步引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # 可以添加MySQL特有的参数
    pool_size=5,  # 连接池大小
    max_overflow=10,  # 超过连接池大小时，最多可创建的连接数
    pool_timeout=30,  # 等待获取连接的超时时间
    pool_recycle=1800  # 连接在池中保持时间（秒）
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