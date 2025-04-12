from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum
from sqlalchemy.orm import relationship
# from .database import Base

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

    # training_records = relationship("TrainingRecord", back_populates="user", cascade="all, delete-orphan",passive_deletes=True)
    # def __repr__(self):
    #     return f"<User(id={self.id}, username={self.username})>"

class TrainingRecord(Base):
    __tablename__ = "training_records"
    
    # filename作为主键
    filename = Column(String(255), primary_key=True, index=True)
    # # 外键关联用户表
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    
    # 基本训练信息
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    activity_type = Column(String(20), nullable=True)
    duration_minutes = Column(Integer, nullable=True)  # 运动时长(分钟)
    
    # # 详细训练数据
    # average_heart_rate = Column(Integer, nullable=True)  # 平均心率
    # max_heart_rate = Column(Integer, nullable=True)  # 最大心率
    
    # # 记录管理
    # created_at = Column(DateTime, server_default=func.now())  # 记录创建时间
    # updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())  # 记录更新时间
    
    # 关系定义 - 建立与用户表的关联
    # user = relationship("User", back_populates="training_records")
    
    # def __repr__(self):
    #     return f"<TrainingRecord(id={self.id}, user_id={self.user_id}, activity={self.activity_type}, duration={self.duration_minutes})>"
    

class TrainingTask(Base):
    __tablename__ = "training_tasks"
    
    id = Column(Integer, primary_key=True, index=True)


    # 外键关联用户表
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # 任务基本信息
    task_name = Column(String(100), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    # 关系定义 - 与用户表建立关联
    user = relationship("User", backref="training_tasks")
    
    # 记录管理
    # created_at = Column(DateTime, server_default=func.now())
    # updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    # def __repr__(self):
    #     return f"<TrainingTask(id={self.id}, user_id={self.user_id}, task_name={self.task_name})>"