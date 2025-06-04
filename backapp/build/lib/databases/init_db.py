import asyncio
import os
import sys
from datetime import datetime, timedelta
from .models import TrainingRecord, User
from .database import SessionLocal
import uuid

"""
AI-generated-content 
tool: ChatGPT 
version: 4o
usage: I used the prompt "提示path不存在，如何解决”"
"""
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
    db = SessionLocal()  # 获取数据库会话

    # 如果没有用户，就创建一个测试用户（user_id = 1）
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        user = User(id=1, username="testuser", email="test@example.com", password="123456")
        db.add(user)
        db.commit()

    now = datetime.now()
    records = []

    # 生成20条模拟数据
    for _ in range(20):
        filename = f"{uuid.uuid4()}.json"
        activity_type = "有氧" if _ % 3 == 0 else "力量" if _ % 3 == 1 else "拉伸"
        duration_minutes = 30 + (_ % 3) * 5  # 随机时长 30-35分钟
        start_time = now - timedelta(days=(_ % 7))  # 每天生成数据
        end_time = start_time + timedelta(minutes=duration_minutes)

        record = TrainingRecord(
            # filename=filename,
            user_id=1,
            start_time=start_time,
            end_time=end_time,
            activity_type=activity_type,
            duration_minutes=duration_minutes,
            distance=round(5 + _ % 3, 2),  # 随机距离
            calories=round(200 + _ * 5, 2),  # 随机卡路里
            average_heart_rate=round(120 + _ % 10, 2),  # 随机心率
            max_heart_rate=round(140 + _ % 15, 2),  # 随机最大心率
            minute_heart_rates={str(i): round(120 + (i % 5), 2) for i in range(1, duration_minutes + 1)}  # 模拟心率数据
        )

        records.append(record)

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
