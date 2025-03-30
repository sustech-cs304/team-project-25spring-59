from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import re
from backapp.auth.token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from backapp.auth.dependencies import get_current_user
# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入数据库模块
from databases.database import get_db
from databases import models, crud
from databases.init_db import init_db
from sqlalchemy.orm import Session

app = FastAPI()
SAVE_DIR = "./TrainMission/posts"
# 启动时初始化数据库
@app.on_event("startup")
def startup_db_client():
    init_db()

# 允许跨域请求，方便前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方式
    allow_headers=["*"],  # 允许所有请求头
)

# 模拟的用户数据库
fake_users_db = {
    "1": {
        "username": "1",
        "email": "test@example.com",
        "password": "1"  # 真实情况应该存储哈希密码
    }
}


# 定义用户模型
class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class SaveMissionRequest(BaseModel):
    fileName: str
    content: str


@app.get("/")
def read_root():
    return {"message": "FastAPI 服务器运行成功！"}


@app.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    print(f"接收到登录请求: {user.username}")
    
    db_user = crud.get_user_by_username(db, username=user.username)
    
    if db_user is None:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 将ORM对象转换为字典，然后比较实际值
    user_dict = db_user.__dict__
    if user_dict["password"] != user.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 创建响应
    return {
        "message": "登录成功", 
        "token": "mock-token",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email
        }
    }


# 注册接口
@app.post("/register")
def register(user: RegisterRequest, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查邮箱是否已存在
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    # 创建新用户
    new_user = crud.create_user(
        db=db,
        username=user.username,
        email=user.email,
        password=user.password
    )
    
    return {"message": "注册成功", "username": new_user.username}

@app.post("/saveMission")
def save_mission(data: SaveMissionRequest, db: Session = Depends(get_db)):
    try:
        file_path = os.path.join(SAVE_DIR, data.fileName)
        file_directory = os.path.dirname(file_path)
        user = db.query(models.User).filter(models.User.id == 1).first()
        if not user:
            print("用户不存在")
        else:
            print("用户存在")   
        # 确保目标目录存在
        os.makedirs(file_directory, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data.content)

        # 提取开始时间
        start_time_match = re.search(r"开始时间\*\*:\s*([^\n]+)", data.content)
        start_time = datetime.fromisoformat(start_time_match.group(1)) if start_time_match else None

        # 提取结束时间
        end_time_match = re.search(r"结束时间\*\*:\s*([^\n]+)", data.content)
        end_time = datetime.fromisoformat(end_time_match.group(1)) if end_time_match else None

        # 提取运动类型
        activity_type_match = re.search(r"运动类型\*\*:\s*([^\n]+)", data.content)
        activity_type = activity_type_match.group(1) if activity_type_match else None

        # 提取时长（分钟）
        duration_match = re.search(r"时长\*\*:\s*(\d+)", data.content)
        duration_minutes = int(duration_match.group(1)) if duration_match else None
        print(duration_minutes)

        # user_id = 1
        # user_id = current_user.id
        # print(f"使用当前登录用户ID: {user_id}")
        # print(f"正则提取结果: 开始时间={start_time}, 结束时间={end_time}, 活动类型={activity_type}, 时长={duration_minutes}")
        db_record = crud.create_training_record(
            db=db,
            user_id=1,
            start_time=start_time if start_time else datetime.now(),
            end_time=end_time if end_time else datetime.now(),
            activity_type=activity_type if activity_type else "未知",
            duration_minutes=duration_minutes if duration_minutes else 0
        )
        return {"message": "文件保存成功", "filePath": file_path, "status": "success"}   
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": "文件保存失败", "error": str(e), "status": "failure"})