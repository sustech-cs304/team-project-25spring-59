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

current_user_id = None
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
    user_id: int

class TrainingTaskCreate(BaseModel):
    task_name: str
    start_time: datetime
    end_time: datetime

class TrainingTaskResponse(BaseModel):
    id: int
    user_id: int
    task_name: str
    start_time: datetime
    end_time: datetime
    created_at: datetime

# 添加请求模型
class UserIdRequest(BaseModel):
    user_id: int

class DeleteRecordRequest(BaseModel):
    filename: str

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
    global current_user_id
    current_user_id = db_user.id    
    # 创建响应
    return {
        "message": "登录成功", 
        "token": "mock-token",  
        "user_id": db_user.id,
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

        user_id = data.user_id
        print(f"保存记录使用的用户ID: {user_id}")
        # user = db.query(models.User).filter(models.User.id == 1).first()
        # if not user:
        #     print("用户不存在")
        # else:
        #     print("用户存在")   
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
            filename=data.fileName,
            user_id=user_id,
            start_time=start_time if start_time else datetime.now(),
            end_time=end_time if end_time else datetime.now(),
            activity_type=activity_type if activity_type else "未知",
            duration_minutes=duration_minutes if duration_minutes else 0
        )
        return {"message": "文件保存成功", "filePath": file_path, "status": "success"}   
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": "文件保存失败", "error": str(e), "status": "failure"})
    

@app.post("/training-tasks", response_model=TrainingTaskResponse)
def create_task(task: TrainingTaskCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """创建新的训练任务"""
    
    user_dict = current_user.__dict__
    user_id = user_dict["id"]
        
    return crud.create_training_task(
        db=db,
        user_id=user_id,
        task_name=task.task_name,
        start_time=task.start_time,
        end_time=task.end_time
    )
@app.get("/training-tasks", response_model=list[TrainingTaskResponse])
def read_tasks(skip: int = 0, limit: int = 100, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取当前用户的所有训练任务"""
    user_dict = current_user.__dict__
    user_id = user_dict["id"]
    tasks = crud.get_training_tasks(db=db, user_id=user_id, skip=skip, limit=limit)
    return tasks

@app.get("/training-tasks/{task_id}", response_model=TrainingTaskResponse)
def read_task(task_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取指定的训练任务"""
    task = crud.get_training_task(db=db, task_id=task_id)
    user_dict = current_user.__dict__
    if task is None or task.__dict__["user_id"] != user_dict["id"]:
        raise HTTPException(status_code=404, detail="训练任务不存在或无权访问")
    return task

@app.put("/training-tasks/{task_id}", response_model=TrainingTaskResponse)
def update_task(task_id: int, task: TrainingTaskCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """更新训练任务"""
    db_task = crud.get_training_task(db=db, task_id=task_id)
    user_dict = current_user.__dict__
    if db_task is None or db_task.__dict__["user_id"] != user_dict["id"]:
        raise HTTPException(status_code=404, detail="训练任务不存在或无权访问")
    
    task_data = task.dict()
    updated_task = crud.update_training_task(db=db, task_id=task_id, task_data=task_data)
    return updated_task

@app.delete("/training-tasks/{task_id}")
def delete_task(task_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """删除训练任务"""
    db_task = crud.get_training_task(db=db, task_id=task_id)
    user_dict = current_user.__dict__
    if db_task is None or db_task.__dict__["user_id"] != user_dict["id"]:
        raise HTTPException(status_code=404, detail="训练任务不存在或无权访问")
    
    success = crud.delete_training_task(db=db, task_id=task_id)
    if success:
        return {"message": "训练任务已成功删除"}
    else:
        raise HTTPException(status_code=500, detail="删除训练任务失败")

@app.post("/generate-user-records")
def generate_user_records(request: UserIdRequest, db: Session = Depends(get_db)):
    """
    根据用户ID生成所有训练记录的MD文件
    """
    try:
        user_id = request.user_id
        # 获取该用户的所有训练记录
        records = crud.get_training_records_by_user(db, user_id)
        print(f"获取到的训练记录: {records}")
        
        if not records:
            return {"message": "未找到该用户的训练记录", "count": 0}
        
        # 确保目录存在
        os.makedirs(SAVE_DIR, exist_ok=True)
        
        generated_files = []
        
        # 为每条记录生成MD文件
        for record in records:
            # 使用数据库中存储的文件名，确保转换为字符串
            filename = str(record.filename)
            
            # 构建MD内容
            md_content = f"""---
title: "{record.activity_type} 运动记录"
date: "{datetime.now().isoformat()}"
---
## 运动详情
- **开始时间**: {record.start_time.isoformat()}
- **结束时间**: {record.end_time.isoformat()}
- **运动类型**: {record.activity_type}
- **时长**: {record.duration_minutes} 分钟
"""
            
            # 保存文件
            file_path = os.path.join(SAVE_DIR, filename)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(md_content)
            
            generated_files.append(filename)
        
        return {
            "message": "成功生成训练记录文件",
            "count": len(generated_files),
            "files": generated_files
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成训练记录失败: {str(e)}")

@app.post("/delete-record")
def delete_record(request: DeleteRecordRequest, db: Session = Depends(get_db)):
    """
    删除指定文件名的训练记录及其文件
    """
    try:
        filename = request.filename
        
        # 1. 先删除文件系统中的文件
        file_path = os.path.join(SAVE_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"已删除文件: {file_path}")
        else:
            print(f"文件不存在: {file_path}")
        
        # 2. 再删除数据库中的记录
        success = crud.delete_training_record(db=db, filename=filename)
        
        if success:
            return {"message": "训练记录已成功删除", "filename": filename}
        else:
            # 如果数据库记录不存在但文件已删除，仍返回成功
            if not os.path.exists(file_path):
                return {"message": "文件已删除，但数据库记录不存在", "filename": filename}
            raise HTTPException(status_code=404, detail="未找到该训练记录")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除训练记录失败: {str(e)}")