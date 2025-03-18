from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    gender = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    height = Column(Float, nullable=True)  
    weight = Column(Float, nullable=True) 
    is_active = Column(Boolean, default=True)