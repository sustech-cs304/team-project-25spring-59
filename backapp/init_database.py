import os
import sys

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

if __name__ == "__main__":
    init_db() 