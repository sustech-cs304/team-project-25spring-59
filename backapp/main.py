from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入数据库模块
from databases.database import get_db
from databases import models, crud
from databases.init_db import init_db
from sqlalchemy.orm import Session

app = FastAPI()

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
