from sqlalchemy.orm import Session
from backapp.databases import models
from datetime import datetime

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


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
        filename: str,
        user_id: int,
        start_time: datetime,
        end_time: datetime,
        activity_type: str,
        duration_minutes: int,
):
    """创建新的训练记录"""
    db_record = models.TrainingRecord(
        filename=filename,
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

def create_training_task(db: Session, 
                         user_id: int, 
                         task_name: str,
                         start_time: datetime,
                         end_time: datetime):
    """创建新的训练任务"""
    db_task = models.TrainingTask(
        user_id=user_id,
        task_name=task_name,
        start_time=start_time,
        end_time=end_time
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_training_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """获取该用户的所有训练任务"""
    return db.query(models.TrainingTask).filter(
        models.TrainingTask.user_id == user_id
    ).offset(skip).limit(limit).all()

def get_training_task(db: Session, task_id: int):
    """获取指定的训练任务"""
    return db.query(models.TrainingTask).filter(models.TrainingTask.id == task_id).first()

def update_training_task(db: Session, task_id: int, task_data: dict):
    """更新训练任务信息"""
    db_task = db.query(models.TrainingTask).filter(models.TrainingTask.id == task_id).first()
    if db_task:
        for key, value in task_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task
def delete_training_task(db: Session, task_id: int):
    """删除指定的训练任务"""
    db_task = db.query(models.TrainingTask).filter(models.TrainingTask.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False

def get_training_records_by_user(db: Session, user_id: int):
    """获取指定用户的所有训练记录"""
    return db.query(models.TrainingRecord).filter(
        models.TrainingRecord.user_id == user_id
    ).all()

def delete_training_record(db: Session, filename: str):
    """删除指定的训练记录"""
    db_record = db.query(models.TrainingRecord).filter(models.TrainingRecord.filename == filename).first()
    if db_record:
        db.delete(db_record)
        db.commit()
        return True
    return False

def update_training_record(db: Session, filename: str, record_data: dict):
    """更新训练记录信息"""
    db_record = db.query(models.TrainingRecord).filter(models.TrainingRecord.filename == filename).first()
    if db_record:
        for key, value in record_data.items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
        return db_record
    return None

def get_training_records_by_date_range(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    """获取用户在指定日期范围内的训练记录"""
    return db.query(models.TrainingRecord).filter(
        models.TrainingRecord.user_id == user_id,
        models.TrainingRecord.start_time >= start_date,
        models.TrainingRecord.start_time <= end_date
    ).all()



