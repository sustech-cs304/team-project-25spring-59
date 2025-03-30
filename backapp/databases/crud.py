from sqlalchemy.orm import Session
from backapp.databases import models
from datetime import datetime

# 用户相关操作
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, username: str, email: str, password: str):
    db_user = models.User(username=username, email=email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_training_record(db: Session,
        user_id: int,
        start_time: datetime,
        end_time: datetime,
        activity_type: str,
        duration_minutes: int,
):
    """创建新的训练记录"""
    db_record = models.TrainingRecord(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        activity_type=activity_type,
        duration_minutes=duration_minutes
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record