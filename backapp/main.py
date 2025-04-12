from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import re
from auth.token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from auth.dependencies import get_current_user
# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入数据库模块
from databases.database import get_db
from databases import models, crud
from databases.init_db import init_db
from sqlalchemy.orm import Session

app = FastAPI()
SAVE_DIR = os.path.join(os.path.dirname(__file__), "TrainMission", "posts")
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
            user_id=1,
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

from pydantic.alias_generators import to_camel
class DTO(BaseModel):
    model_config = {"alias_generator": to_camel, "populate_by_name": True, "from_attributes": True,
                    "json_encoders": {datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}}

# 健身房课程相关模型
class GymCourseResponse(DTO):
    id: int
    gym_id: int
    course_name: str
    coach_name: str
    start_time: datetime
    end_time: datetime
    capacity: int
    current_reservations: int

class CourseReservationCreate(DTO):
    course_id: int

class CourseReservationResponse(DTO):
    id: int
    user_id: int
    course_id: int
    reservation_time: datetime
    status: str

# 健身房预约相关模型
class GymReservationCreate(DTO):
    gym_id: int
    reservation_date: datetime
    start_time: datetime
    end_time: datetime

class GymReservationResponse(DTO):
    id: int
    user_id: int
    gym_id: int
    reservation_date: datetime
    start_time: datetime
    end_time: datetime
    status: str

class GymResponse(DTO):
    id: int
    name: str
    open_time: str  # 格式如: "09:00:00-21:00:00"
    address: str



@app.get("/gym/getCourses", summary="获取健身房课程列表", response_model=list[GymCourseResponse])
async def get_gym_courses(
    gym_id: int,
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取指定健身房的所有课程"""
    courses = crud.get_gym_courses(db=db, gym_id=gym_id, skip=skip, limit=limit)
    return courses

@app.post("/gym/reserveCourse", summary="预约健身课程", response_model=CourseReservationResponse)
async def reserve_course(
    reservation: CourseReservationCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """预约健身课程"""
    user_dict = current_user.__dict__
    user_id = user_dict["id"]
    
    # 创建课程预约
    db_reservation = crud.create_course_reservation(
        db=db,
        user_id=user_id,
        course_id=reservation.course_id
    )
    
    if db_reservation is None:
        raise HTTPException(status_code=400, detail="课程不存在或已满")
    
    return db_reservation

@app.post("/gym/reserveGym", summary="预约健身房", response_model=GymReservationResponse)
async def reserve_gym(
    reservation: GymReservationCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """预约健身房"""
    user_dict = current_user.__dict__
    user_id = user_dict["id"]
    
    # 创建健身房预约
    db_reservation = crud.create_gym_reservation(
        db=db,
        user_id=user_id,
        gym_id=reservation.gym_id,
        reservation_date=reservation.reservation_date,
        start_time=reservation.start_time,
        end_time=reservation.end_time
    )
    
    if db_reservation is None:
        raise HTTPException(status_code=400, detail="健身房不存在或预约失败")
    
    return db_reservation

@app.get("/gym/getGyms", summary="获取健身房列表", response_model=list[GymResponse])
async def get_gyms(
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 获取用户信息
    # user_dict = current_user.__dict__
    # user_id = user_dict["id"]
    #
    # # 调用推荐函数，获取个性化推荐的健身房列表
    # gyms = crud.recommend_gyms_for_user(
    #     db=db,
    #     user_id=user_id,
    #     skip=skip,
    #     limit=limit
    # )
    gyms = crud.get_gyms(db, skip, limit)
    return gyms

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)