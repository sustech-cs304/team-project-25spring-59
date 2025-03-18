from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    # 为String类型指定长度，MySQL要求String必须有长度限制
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    gender = Column(String(10), nullable=True)
    age = Column(Integer, nullable=True)
    height = Column(Float, nullable=True)  
    weight = Column(Float, nullable=True) 
    is_active = Column(Boolean, default=True)
    
    # 可以添加MySQL特有的表选项
    __table_args__ = {
        'mysql_engine': 'InnoDB',  # 使用InnoDB引擎
        'mysql_charset': 'utf8mb4',  # 使用utf8mb4字符集
        'mysql_collate': 'utf8mb4_unicode_ci'  # 使用unicode校对规则
    }