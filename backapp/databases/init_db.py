import asyncio
import os
import sys
from datetime import datetime, timedelta
from .models import TrainingRecord, User
from .database import SessionLocal
import uuid

# 确保项目根目录在Python路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from backapp.databases.database import engine
from backapp.databases.models import Base

def init_db():
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("Database initialized!")





def insert_mock_data():
    db = SessionLocal()

    # 如果没有用户，就创建一个测试用户（user_id = 1）
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        user = User(id=1, username="testuser", email="test@example.com", password="123456")
        db.add(user)
        db.commit()

    now = datetime.now()
    records = [
        TrainingRecord(
            filename=f"{uuid.uuid4()}.json",
            user_id=1,
            start_time=now - timedelta(days=5),
            end_time=now - timedelta(days=5, minutes=-30),
            activity_type="有氧",
            duration_minutes=30
        ),
        TrainingRecord(
            filename=f"{uuid.uuid4()}.json",
            user_id=1,
            start_time=now - timedelta(days=4),
            end_time=now - timedelta(days=4, minutes=-45),
            activity_type="力量",
            duration_minutes=45
        ),
        TrainingRecord(
            filename=f"{uuid.uuid4()}.json",
            user_id=1,
            start_time=now - timedelta(days=3),
            end_time=now - timedelta(days=3, minutes=-25),
            activity_type="拉伸",
            duration_minutes=25
        ),
    ]

    # 避免重复插入（检查是否已有记录）
    if not db.query(TrainingRecord).filter(TrainingRecord.user_id == 1).first():
        db.add_all(records)
        db.commit()
        print("✅ 模拟训练数据已插入")
    else:
        print("ℹ️ 已存在训练数据，跳过插入")

    db.close()


# 如果直接运行此文件，则初始化数据库
if __name__ == "__main__":
    init_db()
