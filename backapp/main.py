from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import re
from backapp.auth.token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from backapp.auth.dependencies import get_current_user

from typing import List, Optional
from sqlalchemy.orm import joinedload
from typing import Optional 

from fastapi import UploadFile, File, Form
import os, uuid, shutil
from fastapi.staticfiles import StaticFiles

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入数据库模块
from databases.database import get_db, SessionLocal
from databases import models, crud
from databases.init_db import init_db, insert_mock_data
from sqlalchemy.orm import Session

current_user_id = None
app = FastAPI()
SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../TrainMission/posts")
SAVE_DIR = os.path.abspath(SAVE_DIR)
print("保存路径为：", SAVE_DIR)
# 启动时初始化数据库
@app.on_event("startup")
def startup_db_client():
    init_db()
    # insert_mock_data()  # 👈 启动时自动插入数据
    # 执行 test.sql 文件
    from sqlalchemy import text
    from databases.database import SessionLocal
    
    try:
        db = SessionLocal()
        with open('test.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # 按分号分割执行多条SQL语句
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
        for stmt in statements:
            db.execute(text(stmt))
        
        db.commit()
        print("成功执行 test.sql 文件")
        
        # 更新training_records表的is_completed和record_type字段
        try:
            # 获取当前时间
            now = datetime.now()
            
            # 查询所有training_records记录
            records = db.query(models.TrainingRecord).all()
            updated_count = 0
            
            for record in records:
                # 确保datetime对象是naive的(不带时区)
                record_start_time = record.start_time
                if record_start_time.tzinfo is not None:
                    record_start_time = record_start_time.replace(tzinfo=None)
                
                # 根据start_time与当前时间比较设置字段
                if record_start_time < now:
                    record.is_completed = True
                    record.record_type = "record"
                else:
                    record.is_completed = False
                    record.record_type = "plan"
                updated_count += 1
                
            db.commit()
            print(f"成功更新 {updated_count} 条训练记录的状态")
        except Exception as e:
            print(f"更新训练记录失败: {e}")
        
    except Exception as e:
        print(f"执行 SQL 脚本出错: {e}")
    finally:
        db.close()

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

"""
AI-generated-content 
tool: ChatGPT 
version: 4o
usage: I used the prompt "使用python写一个BaseModel，内容是username, email, password"", and 
directly copy the code from its response 
"""
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class SaveMissionRequest(BaseModel):
    user_id: int
    start_time: datetime
    end_time: datetime
    activity_type: str
    duration_minutes: int
    calories: Optional[int] = None 
    average_heart_rate: Optional[int] = None
    is_completed: bool = False

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
    record_id: int

class EditRecordRequest(BaseModel):
    record_id: int
    user_id: int
    start_time: datetime | None = None
    end_time: datetime | None = None
    activity_type: str | None = None
    duration_minutes: int | None = None
    calories: int | None = None
    average_heart_rate: int | None = None
    is_completed: bool | None = None

class WeeklyPlanRequest(BaseModel):
    user_id: int
    date_str: str  # 格式为"x月x日"

class DailyPlanRequest(BaseModel):
    user_id: int
    date_str: str  # 格式为"x年x月x日"

class ChallengeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    challenge_type: str  # 'distance', 'calories', 'workouts', 'duration'
    target_value: float
    created_by: int

class ChallengeResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    challenge_type: str
    target_value: float
    created_by: int
    
    class Config:
        from_attributes = True

class JoinChallengeRequest(BaseModel):
    challenge_id: int
    user_id: int 

class UserChallengeResponse(BaseModel):
    id: int
    user_id: int
    challenge_id: int
    join_date: datetime
    current_value: float
    completed: bool
    
    class Config:
        from_attributes = True

class UpdateChallengeProgressRequest(BaseModel):
    challenge_id: int
    user_id: int
    current_value: float

class ChallengeDetail(BaseModel):
    challenge_id: int

class UserChallengeDetail(BaseModel):
    user_id: int

class EndChallengeRequest(BaseModel):
    challenge_id: int

class RecordIdRequest(BaseModel):
    record_id: int

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

@app.post("/generate-user-records/completed")
def get_user_completed_records(request: UserIdRequest, db: Session = Depends(get_db)):
    """获取指定用户的已完成训练记录（record_type是record的所有记录）"""
    try:
        # 获取当前时间用于比较
        now = datetime.now()
        
        # 获取用户的训练记录 - 已完成记录
        records = db.query(models.TrainingRecord).filter(
            models.TrainingRecord.user_id == request.user_id,
            models.TrainingRecord.record_type == "record"
        ).all()
        
        # 格式化返回结果
        result = []
        for record in records:
            record_dict = {
                "id": record.id,
                "user_id": record.user_id,
                "start_time": record.start_time,
                "end_time": record.end_time,
                "activity_type": record.activity_type,
                "duration_minutes": record.duration_minutes,
                "is_completed": record.is_completed,
                "record_type": record.record_type,
                "reminder_time": record.reminder_time,
                "distance": record.distance,
                "calories": record.calories,
                "average_heart_rate": record.average_heart_rate,
                "max_heart_rate": record.max_heart_rate,
                "minute_heart_rates": record.minute_heart_rates if record.minute_heart_rates else {}
            }
            result.append(record_dict)
        
        return {"records": result, "count": len(result)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取已完成训练记录失败: {str(e)}")

@app.post("/generate-user-records/upcoming-plans")
def get_user_upcoming_plans(request: UserIdRequest, db: Session = Depends(get_db)):
    """获取指定用户的即将进行的计划（record_type是plan，is_completed是False，且end_time不早于当天时间一天以上）"""
    try:
        # 获取当前时间用于比较
        now = datetime.now()
        one_day_ago = now - timedelta(days=1)
        
        # 获取用户的训练记录 - 即将进行的计划
        records = db.query(models.TrainingRecord).filter(
            models.TrainingRecord.user_id == request.user_id,
            models.TrainingRecord.record_type == "plan",
            models.TrainingRecord.is_completed == False,
            models.TrainingRecord.end_time >= one_day_ago
        ).all()
        
        # 格式化返回结果
        result = []
        for record in records:
            record_dict = {
                "id": record.id,
                "user_id": record.user_id,
                "start_time": record.start_time,
                "end_time": record.end_time,
                "activity_type": record.activity_type,
                "duration_minutes": record.duration_minutes,
                "is_completed": record.is_completed,
                "record_type": record.record_type,
                "reminder_time": record.reminder_time,
                "distance": record.distance,
                "calories": record.calories,
                "average_heart_rate": record.average_heart_rate,
                "max_heart_rate": record.max_heart_rate,
                "minute_heart_rates": record.minute_heart_rates if record.minute_heart_rates else {}
            }
            result.append(record_dict)
        
        return {"records": result, "count": len(result)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取即将进行的计划失败: {str(e)}")

@app.post("/generate-user-records/missed-plans")
def get_user_missed_plans(request: UserIdRequest, db: Session = Depends(get_db)):
    """获取指定用户的已错过的计划（record_type是plan，end_time早于当前时间一天以上，且is_completed是False）"""
    try:
        # 获取当前时间用于比较
        now = datetime.now()
        one_day_ago = now - timedelta(days=1)
        
        # 获取用户的训练记录 - 已错过的计划
        records = db.query(models.TrainingRecord).filter(
            models.TrainingRecord.user_id == request.user_id,
            models.TrainingRecord.record_type == "plan",
            models.TrainingRecord.is_completed == False,
            models.TrainingRecord.end_time < one_day_ago
        ).all()
        
        # 格式化返回结果
        result = []
        for record in records:
            record_dict = {
                "id": record.id,
                "user_id": record.user_id,
                "start_time": record.start_time,
                "end_time": record.end_time,
                "activity_type": record.activity_type,
                "duration_minutes": record.duration_minutes,
                "is_completed": record.is_completed,
                "record_type": record.record_type,
                "reminder_time": record.reminder_time,
                "distance": record.distance,
                "calories": record.calories,
                "average_heart_rate": record.average_heart_rate,
                "max_heart_rate": record.max_heart_rate,
                "minute_heart_rates": record.minute_heart_rates if record.minute_heart_rates else {}
            }
            result.append(record_dict)
        
        return {"records": result, "count": len(result)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取已错过的计划失败: {str(e)}")

@app.post("/generate-user-records")
def generate_user_records(request: UserIdRequest, db: Session = Depends(get_db)):
    """获取指定用户的所有训练记录"""
    try:
        # 获取用户的训练记录
        records = crud.get_training_records_by_user(db, user_id=request.user_id)
        
        # 格式化返回结果
        result = []
        for record in records:
            record_dict = {
                "id": record.id,
                "user_id": record.user_id,
                "start_time": record.start_time,
                "end_time": record.end_time,
                "activity_type": record.activity_type,
                "duration_minutes": record.duration_minutes,
                "is_completed": record.is_completed,
                "record_type": record.record_type,
                "reminder_time": record.reminder_time,
                "distance": record.distance,
                "calories": record.calories,
                "average_heart_rate": record.average_heart_rate,
                "max_heart_rate": record.max_heart_rate,
                "minute_heart_rates": record.minute_heart_rates if record.minute_heart_rates else {}
            }
            result.append(record_dict)
        
        return {"records": result, "count": len(result)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取训练记录失败: {str(e)}")

@app.post("/saveMission")
def save_mission(data: SaveMissionRequest, db: Session = Depends(get_db)):
    try:
        user_id = data.user_id
        print(f"保存记录使用的用户ID: {user_id}")
        
        # 直接创建数据库记录，不再需要文件操作
        db_record = crud.create_training_record(
            db=db,
            user_id=user_id,
            start_time=data.start_time,
            end_time=data.end_time,
            activity_type=data.activity_type,
            duration_minutes=data.duration_minutes,
            calories=data.calories,
            average_heart_rate=data.average_heart_rate,
            is_completed=data.is_completed
        )
        
        return {
            "message": "训练记录保存成功", 
            "record_id": db_record.id,
            "record_type": db_record.record_type,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": "保存失败", "error": str(e), "status": "failure"})
    

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
    user_id: int
    course_id: int

class CourseReservationResponse(DTO):
    id: int
    user_id: int
    course_id: int
    reservation_time: datetime
    status: str

# 健身房预约相关模型
class GymReservationCreate(DTO):
    user_id: int
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

class ReservedCourseResponse(DTO):
    course_id: int
    gym_id: int
    course_name: str
    start_time: datetime
    end_time: datetime
    coach_name: str
    reservation_time: datetime

class CancelCourseReservationRequest(DTO):
    user_id: int
    course_id: int


@app.get("/gym/getCourses/{gym_id}", summary="获取健身房课程列表", response_model=list[GymCourseResponse])
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
    db: Session = Depends(get_db),
):
    """预约健身课程"""
    
    # 创建课程预约
    db_reservation = crud.create_course_reservation(
        db=db,
        user_id=reservation.user_id,
        course_id=reservation.course_id
    )
    
    if db_reservation is None:
        raise HTTPException(status_code=400, detail="课程不存在或已满")
    
    return db_reservation

from sqlalchemy.orm import aliased
@app.get(
    "/course/getReservedCourses/{user_id}",
    summary="获取个人预约课程",
    response_model=list[ReservedCourseResponse],
)
def get_reserved_courses(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    返回指定用户已预约的课程列表  
    直接联表 `course_reservations` ➜ `gym_courses`。
    """
    Course = aliased(models.GymCourse)
    Reservation = aliased(models.CourseReservation)

    rows = (
        db.query(
            Reservation.course_id,
            Course.gym_id,
            Course.course_name,
            Course.start_time,
            Course.end_time,
            Course.coach_name,
            Reservation.reservation_time,
        )
        .join(Course, Reservation.course_id == Course.id)
        .filter(Reservation.user_id == user_id)
        .order_by(Reservation.reservation_time.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # rows 是 Row 对象列表，直接转 dict/模型
    return [ReservedCourseResponse(**row._mapping) for row in rows]

@app.post("/gym/cancelCourseReservation", summary="取消健身课程预约")
def cancel_course_reservation(
    request: CancelCourseReservationRequest,
    db: Session = Depends(get_db),
):
    """
    根据 user_id 和 course_id 取消健身课程预约
    """
    reservation = db.query(models.CourseReservation).filter(
        models.CourseReservation.user_id == request.user_id,
        models.CourseReservation.course_id == request.course_id
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="找不到对应的预约记录")
    
    # 找到对应课程
    course = db.query(models.GymCourse).filter(models.GymCourse.id == request.course_id).first()
    if course and course.current_reservations > 0:
        course.current_reservations -= 1

    # 删除预约
    db.delete(reservation)
    db.commit()

    return {"message": "取消预约成功", "course_id": request.course_id}

@app.post("/gym/reserveGym", summary="预约健身房", response_model=GymReservationResponse)
async def reserve_gym(
    reservation: GymReservationCreate,
    db: Session = Depends(get_db),
):
    """预约健身房"""
    
    # 创建健身房预约
    db_reservation = crud.create_gym_reservation(
        db=db,
        user_id=reservation.user_id,
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


@app.post("/delete-record")
def delete_record(request: DeleteRecordRequest, db: Session = Depends(get_db)):
    """删除指定ID的训练记录"""
    try:
        success = crud.delete_training_record(db=db, record_id=request.record_id)
        
        if success:
            return {"message": "训练记录已成功删除", "record_id": request.record_id}
        else:
            raise HTTPException(status_code=404, detail="未找到该训练记录")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除训练记录失败: {str(e)}")

@app.post("/edit-record")
def edit_record(data: EditRecordRequest, db: Session = Depends(get_db)):
    """编辑指定ID的训练记录"""
    try:
        # 构建要更新的数据
        record_data = {k: v for k, v in data.dict().items() if v is not None and k != 'record_id'}
        
        # 更新数据库记录
        updated_record = crud.update_training_record(db=db, record_id=data.record_id, record_data=record_data)
        
        if updated_record:
            return {
                "message": "训练记录已成功更新", 
                "record_id": data.record_id,
                "record_type": updated_record.record_type,
                "status": "success"
            }
        else:
            raise HTTPException(status_code=404, detail="未找到该训练记录")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新训练记录失败: {str(e)}")

"""
AI-generated-content 
tool: ChatGPT 
version: 4o
usage: I used the prompt "我需要使用python实现一个功能：解析"x月y日的格式，提取x和y"", and 
directly copy the code from its response 
"""
@app.post("/get-weekly-plan")
def get_weekly_plan(request: WeeklyPlanRequest, db: Session = Depends(get_db)):
    """
    获取指定用户和日期所在周的训练计划
    """
    try:
        user_id = request.user_id
        date_str = request.date_str
        
        # 1. 解析日期字符串
        current_year = datetime.now().year
        # 处理"x月x日"格式
        match = re.match(r'(\d+)月(\d+)日', date_str)
        if not match:
            raise HTTPException(status_code=400, detail="日期格式不正确，应为'x月x日'")
        
        month, day = int(match.group(1)), int(match.group(2))
        
        # 创建日期对象
        try:
            given_date = datetime(current_year, month, day)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"无效日期: {str(e)}")
        
        # 2. 计算这一周的起止日期（周一到周日）
        # 计算给定日期是周几（0是周一，6是周日）
        weekday = given_date.weekday()
        
        # 计算这周的周一日期
        monday = given_date - timedelta(days=weekday)
        
        # 生成周一到周日的日期列表
        week_dates = [(monday + timedelta(days=i)).date() for i in range(7)]
        
        # 3. 查询用户在这周每天的训练记录
        week_start = datetime.combine(week_dates[0], datetime.min.time())
        week_end = datetime.combine(week_dates[6], datetime.max.time())
        
        records = crud.get_training_records_by_date_range(
            db=db, 
            user_id=user_id,
            start_date=week_start,
            end_date=week_end
        )
        
        # 4. 按天组织数据
        week_tasks = []
        weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        
        for i, date in enumerate(week_dates):
            date_records = [
                f"{record.activity_type} {record.duration_minutes}分钟" 
                for record in records 
                if record.start_time.date() == date
            ]
            
            # 如果没有记录，提供一个默认值
            if not date_records:
                date_records = ["暂无训练"]
                
            week_tasks.append({
                "title": weekday_names[i],
                "date": f"{date.month}月{date.day}日",
                "tasks": date_records
            })
        
        return {
            "week_start": week_dates[0].strftime("%Y-%m-%d"),
            "week_end": week_dates[6].strftime("%Y-%m-%d"),
            "weekTasks": week_tasks
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取周计划失败: {str(e)}")



@app.post("/stats/summary")
def get_training_summary(data: UserIdRequest, db: Session = Depends(get_db)):
    print(f"[summary] 收到 user_id: {data.user_id}")

    # 获取训练记录
    records = crud.get_training_records_by_user(db, user_id=data.user_id)
    print(f"[summary] 获取到记录数: {len(records)}")

    # 计算总训练时长和实际卡路里
    total_minutes = sum([r.duration_minutes or 0 for r in records])
    total_calories_actual = sum([r.calories or 0 for r in records])
    average_heart_rates = [r.average_heart_rate for r in records if r.average_heart_rate]
    max_heart_rates = [r.max_heart_rate for r in records if r.max_heart_rate]

    # 输出调试信息
    print(f"[summary] 总训练时长: {total_minutes} 分钟")
    print(f"[summary] 实际卡路里总和: {total_calories_actual} kcal")

    # 获取用户数据
    user = crud.get_user_by_id(db, data.user_id)
    if not user:
        print("[summary] 用户不存在")
        raise HTTPException(status_code=404, detail="用户不存在")

    weight = user.weight or 60  # 默认体重60kg
    MET = 8  # MET值，这里假设为8
    total_calories_estimated = MET * weight * (total_minutes / 60)

    # 输出估算卡路里
    print(f"[summary] 估算卡路里: {total_calories_estimated} kcal")

    # 返回统计信息
    return {
        "total_minutes": total_minutes,
        "estimated_calories": round(total_calories_estimated, 2),
        "actual_calories": total_calories_actual,
        "average_heart_rate": int(sum(average_heart_rates) / len(average_heart_rates)) if average_heart_rates else None,
        "max_heart_rate": max(max_heart_rates) if max_heart_rates else None
    }


@app.post("/stats/weekly-trend")
def get_weekly_trend(data: UserIdRequest, start_date: str, end_date: str, db: Session = Depends(get_db)):
    print(f"[trend] 收到 user_id: {data.user_id}")

    try:
        # 将传入的字符串日期转换为 datetime 对象
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式错误，应为 YYYY-MM-DD")

    print(f"[trend] 查询时间范围: {start_date.date()} 到 {end_date.date()}")

    # 获取指定日期范围的训练记录
    records = crud.get_training_records_by_date_range(
        db, user_id=data.user_id, start_date=start_date, end_date=end_date
    )
    print(f"[trend] 获取到记录数: {len(records)}")

    # 初始化趋势数据
    trend = { (start_date + timedelta(days=i)).strftime("%Y-%m-%d"): {
            "duration_minutes": 0,
            "calories": 0,
            "avg_heart_rate": [],
            "max_heart_rate": []
        } for i in range((end_date - start_date).days + 1)}

    # 处理记录并填充趋势数据
    for r in records:
        date_str = r.start_time.strftime("%Y-%m-%d")
        trend[date_str]["duration_minutes"] += r.duration_minutes or 0
        trend[date_str]["calories"] += r.calories or 0
        if r.average_heart_rate:
            trend[date_str]["avg_heart_rate"].append(r.average_heart_rate)
        if r.max_heart_rate:
            trend[date_str]["max_heart_rate"].append(r.max_heart_rate)

    # 计算平均心率和最大心率
    for day_data in trend.values():
        avg_list = day_data["avg_heart_rate"]
        max_list = day_data["max_heart_rate"]
        day_data["avg_heart_rate"] = int(sum(avg_list) / len(avg_list)) if avg_list else None
        day_data["max_heart_rate"] = max(max_list) if max_list else None

    print(f"[trend] 构造出的趋势数据: {trend}")
    return trend

@app.post("/get-daily-plan")
def get_daily_plan(request: DailyPlanRequest, db: Session = Depends(get_db)):
    """
    获取指定用户和日期的训练计划
    """
    try:
        user_id = request.user_id
        date_str = request.date_str
        
        # 1. 解析日期字符串
        # 处理"x年x月x日"格式
        match = re.match(r'(\d+)年(\d+)月(\d+)日', date_str)
        if not match:
            raise HTTPException(status_code=400, detail="日期格式不正确，应为'x年x月x日'")
        
        year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
        
        # 创建日期对象
        try:
            given_date = datetime(year, month, day)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"无效日期: {str(e)}")
        
        # 2. 查询用户在该日期的训练记录
        records = crud.get_training_records_by_date(
            db=db, 
            user_id=user_id,
            date=given_date.date()
        )
        
        # 3. 格式化返回数据
        training_items = [
            f"{record.activity_type} {record.duration_minutes}分钟" 
            for record in records
        ]
        
        # 如果没有记录，提供一个默认值
        if not training_items:
            training_items = ["暂无训练"]
        
        return {
            "date": date_str,
            "full_date": given_date.strftime("%Y-%m-%d"),
            "training_items": training_items
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取日计划失败: {str(e)}")


class CommentResponse(DTO):
    user_id: int
    user_name: str
    comment: str
    time: datetime


class PostResponse(DTO):
    post_id: int
    user_id: int
    user_name: str
    content: str
    time: datetime
    img_list: Optional[List[dict]] = []  # [{"img": "http://..."}, ...]
    comments: List[CommentResponse] = []


class PostCreateRequest(DTO):
    user_id: int
    content: str
    img_list: Optional[List[str]] = None  # ["http://...", "http://..."]


class CommentCreateRequest(DTO):
    user_id: int
    comment: str


def _serialize_comment(c: models.Comment) -> CommentResponse:
    return CommentResponse(
        user_id=c.user_id,
        user_name=c.user.username,
        comment=c.content,
        time=c.created_at,
    )


def _serialize_post(p: models.Post) -> PostResponse:
    return PostResponse(
        post_id=p.id,
        user_id=p.user_id,
        user_name=p.user.username,
        content=p.content,
        time=p.created_at,
        img_list=[{"img": img.url} for img in p.images],  # 使用 PostImage.url
        comments=[
            _serialize_comment(c)
            for c in sorted(p.comments, key=lambda x: x.created_at, reverse=True)
        ],
    )

def _get_post_full(db: Session, post_id: int) -> models.Post:
    post = (
        db.query(models.Post)
        .options(
            joinedload(models.Post.comments).joinedload(models.Comment.user),
            joinedload(models.Post.user),
            joinedload(models.Post.images),  # 加载 PostImage 列表
        )
        .filter(models.Post.id == post_id)
        .first()
    )
    if not post:
        raise HTTPException(404, "Post not found")
    return post

# -------------------------------------------------
# 动态分享接口
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_DIR = os.path.join(STATIC_DIR, "uploads")
BASE_URL = "http://10.26.63.155:8000"  # 部署时替换成你的域名或IP
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.post("/posts", response_model=PostResponse)
def create_post_api(
    user_id: int = Form(...),
    content: str = Form(...),
    files: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
):
    
    db_post = crud.create_post(db=db, user_id=user_id, content=content)

    if files:
        for file in files:
            filename = f"{uuid.uuid4().hex}_{file.filename}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            image_url = f"/static/uploads/{filename}"
            db_image = models.PostImage(post_id=db_post.id, url=image_url)
            db.add(db_image)

    db.commit()
    return _serialize_post(_get_post_full(db, db_post.id))


@app.get("/posts", response_model=list[PostResponse])
def list_posts_api(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    posts = (
        db.query(models.Post)
        .options(
            joinedload(models.Post.comments).joinedload(models.Comment.user),
            joinedload(models.Post.user),
            joinedload(models.Post.images),  # 加载多图
        )
        .order_by(models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [_serialize_post(p) for p in posts]


@app.post("/posts/{post_id}/comments", response_model=CommentResponse)
def add_comment_api(
    post_id: int,
    body: CommentCreateRequest,
    db: Session = Depends(get_db),
):
    cmt = crud.add_comment(db, user_id=body.user_id, post_id=post_id, content=body.comment)
    return _serialize_comment(cmt)


@app.get("/posts/{post_id}/comments", response_model=list[CommentResponse])
def list_comments_api(post_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    post = _get_post_full(db, post_id)
    cmts = sorted(post.comments, key=lambda x: x.created_at, reverse=True)[skip : skip + limit]
    return [_serialize_comment(c) for c in cmts]


@app.post("/challenges", response_model=ChallengeResponse)
def create_challenge(challenge: ChallengeCreate, db: Session = Depends(get_db)):
    """创建新挑战"""
    try:
        # 验证日期
        if challenge.start_date >= challenge.end_date:
            raise HTTPException(status_code=400, detail="结束日期必须晚于开始日期")
        
        # 验证挑战类型
        valid_types = ['distance', 'calories', 'workouts', 'duration']
        if challenge.challenge_type not in valid_types:
            raise HTTPException(status_code=400, detail=f"挑战类型必须是以下之一: {', '.join(valid_types)}")
        
        # 创建挑战
        
        description = challenge.description if challenge.description is not None else ""
        db_challenge = crud.create_challenge(
            db=db,
            title=challenge.title,
            description=description,
            start_date=challenge.start_date,
            end_date=challenge.end_date,
            challenge_type=challenge.challenge_type,
            target_value=challenge.target_value,
            created_by=challenge.created_by,
        )
        return db_challenge
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建挑战失败: {str(e)}")

@app.post("/challenges/join", response_model=UserChallengeResponse)
def join_challenge(request: JoinChallengeRequest, db: Session = Depends(get_db)):
    """用户加入挑战"""
    try:
        # 检查挑战是否存在
        challenge = db.query(models.Challenge).filter(models.Challenge.id == request.challenge_id).first()
        if not challenge:
            raise HTTPException(status_code=404, detail="挑战不存在")
        
        
        # 检查挑战是否已结束
        if challenge.end_date < datetime.now():
            raise HTTPException(status_code=400, detail="此挑战已结束，无法加入")
        
        # 加入挑战
        user_challenge = crud.join_challenge(
            db=db,
            user_id=request.user_id,
            challenge_id=request.challenge_id
        )
        
        return user_challenge
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"加入挑战失败: {str(e)}")
    
@app.get("/challenges/all")
def get_all_challenges(db: Session = Depends(get_db)):
    """获取所有挑战的详细记录"""
    try:
        # 查询所有挑战
        challenges = db.query(models.Challenge).all()
        
        result = []
        
        # 为每个挑战获取详细信息
        for challenge in challenges:
            # 获取参与者数量
            participants_count = db.query(models.UserChallenge).filter(
                models.UserChallenge.challenge_id == challenge.id
            ).count()
            
            # 获取创建者信息
            creator = db.query(models.User).filter(models.User.id == challenge.created_by).first()
            creator_name = creator.username if creator else "未知用户"
            
            # 获取挑战完成率
            completed_count = db.query(models.UserChallenge).filter(
                models.UserChallenge.challenge_id == challenge.id,
                models.UserChallenge.completed == True
            ).count()
            
            completion_rate = (completed_count / participants_count) * 100 if participants_count > 0 else 0
            
            # 获取排行榜前3名
            leaderboard_query = db.query(
                models.UserChallenge,
                models.User.username
            ).join(
                models.User, models.UserChallenge.user_id == models.User.id
            ).filter(
                models.UserChallenge.challenge_id == challenge.id
            ).order_by(
                models.UserChallenge.current_value.desc()
            ).limit(3).all()
            
            top_performers = [
                {
                    "user_id": entry.UserChallenge.user_id,
                    "username": entry.username,
                    "current_value": entry.UserChallenge.current_value,
                    "completed": entry.UserChallenge.completed
                }
                for entry in leaderboard_query
            ]
            now = datetime.now()
        
            
            # 构建挑战详情
            challenge_detail = {
                "id": challenge.id,
                "title": challenge.title,
                "description": challenge.description,
                "start_date": challenge.start_date,
                "end_date": challenge.end_date,
                "challenge_type": challenge.challenge_type,
                "target_value": challenge.target_value,                
                "created_by": challenge.created_by,
                "creator_name": creator_name,
                "status": challenge.status,
                "participants_count": participants_count,
                "completion_rate": completion_rate,
                "top_performers": top_performers,
                "days_remaining": (challenge.end_date - now).days if now < challenge.end_date else 0
            }
            
            result.append(challenge_detail)
        
        return {"challenges": result, "total_count": len(result)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取挑战列表失败: {str(e)}")
    
@app.post("/challenges/update-progress")
def update_challenge_progress(request: UpdateChallengeProgressRequest, db: Session = Depends(get_db)):
    """更新用户在挑战中的进度"""
    try:
        # 检查挑战是否存在
        challenge = db.query(models.Challenge).filter(models.Challenge.id == request.challenge_id).first()
        if not challenge:
            raise HTTPException(status_code=404, detail="挑战不存在")
        
        # 检查用户是否参与该挑战
        user_challenge = db.query(models.UserChallenge).filter(
            models.UserChallenge.user_id == request.user_id,
            models.UserChallenge.challenge_id == request.challenge_id
        ).first()
        
        if not user_challenge:
            raise HTTPException(status_code=404, detail="用户未参与此挑战")
        
        # 更新进度
        user_challenge.current_value = request.current_value
        
        # 检查是否完成挑战
        if request.current_value >= challenge.target_value:
            user_challenge.completed = True
        
        db.commit()
        db.refresh(user_challenge)
        
        # 计算进度百分比
        progress = min(100, (user_challenge.current_value / challenge.target_value) * 100) if challenge.target_value > 0 else 0
        
        return {
            "message": "进度已更新",
            "current_value": user_challenge.current_value,
            "completed": user_challenge.completed,
            "progress": progress
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新挑战进度失败: {str(e)}")


@app.post("/challenges/detail")
def get_challenge_detail(request: ChallengeDetail, db: Session = Depends(get_db)):
    """获取挑战详情，包括参与者数量和完整排行榜"""
    try:
        # 获取挑战信息
        challenge = db.query(models.Challenge).filter(models.Challenge.id == request.challenge_id).first()
        if not challenge:
            raise HTTPException(status_code=404, detail="挑战不存在")
        
        # 获取参与者数量
        participants_count = db.query(models.UserChallenge).filter(
            models.UserChallenge.challenge_id == request.challenge_id
        ).count()


        
        # 初始化响应
        response = {
            "challenge": {
                "id": challenge.id,
                "title": challenge.title,
                "description": challenge.description,
                "start_date": challenge.start_date,
                "end_date": challenge.end_date,
                "status": challenge.status,
                "challenge_type": challenge.challenge_type,
                "target_value": challenge.target_value,
                "created_by": challenge.created_by,
            },
            "participants_count": participants_count,
            "leaderboard": []
        }
        
        
        # 获取完整排行榜（所有参与者）
        leaderboard_query = db.query(
            models.UserChallenge,
            models.User.username
        ).join(
            models.User, models.UserChallenge.user_id == models.User.id
        ).filter(
            models.UserChallenge.challenge_id == request.challenge_id
        ).order_by(
            models.UserChallenge.current_value.desc()
        ).all()
        
        # 格式化排行榜
        response["leaderboard"] = [
            {
                "user_id": entry.UserChallenge.user_id,
                "username": entry.username,
                "current_value": entry.UserChallenge.current_value,
                "completed": entry.UserChallenge.completed,
                "progress": min(100, (entry.UserChallenge.current_value / challenge.target_value) * 100) if challenge.target_value > 0 else 0
            }
            for entry in leaderboard_query
        ]
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取挑战详情失败: {str(e)}")
    

@app.post("/challenges/my", response_model=list[ChallengeResponse])
def my_challenges(request: UserChallengeDetail, db: Session = Depends(get_db)):
    """获取指定用户参与的挑战"""
    try:
        # 查询用户参与的所有挑战ID
        user_challenges = db.query(models.UserChallenge).filter(
            models.UserChallenge.user_id == request.user_id
        ).all()
        
        challenge_ids = [uc.challenge_id for uc in user_challenges]
        
        # 获取这些挑战的详细信息
        challenges = db.query(models.Challenge).filter(
            models.Challenge.id.in_(challenge_ids)
        ).all()
        
        return challenges
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取我的挑战失败: {str(e)}")

@app.post("/challenges/end")
def end_challenge(request: EndChallengeRequest, db: Session = Depends(get_db)):
    """结束挑战并计算每个参与者的得分，更新到用户表中"""
    try:
        # 获取挑战信息
        challenge = db.query(models.Challenge).filter(models.Challenge.id == request.challenge_id).first()
        if not challenge:
            raise HTTPException(status_code=404, detail="挑战不存在")
        
        # 设置挑战结束时间为当前时间（如果提前结束）
        if challenge.end_date > datetime.now():
            challenge.end_date = datetime.now()
        challenge.status = "已结束"
        db.commit()
        
        # 获取所有参与者，按完成值排序
        participants = db.query(
            models.UserChallenge,
            models.User
        ).join(
            models.User, models.UserChallenge.user_id == models.User.id
        ).filter(
            models.UserChallenge.challenge_id == request.challenge_id
        ).order_by(
            models.UserChallenge.current_value.desc()
        ).all()
        
        results = []
        
        # 计算每个参与者的得分
        for rank, p in enumerate(participants):
            user_challenge = p.UserChallenge
            user = p.User
            completion_ratio = min(1.0, user_challenge.current_value / challenge.target_value) if challenge.target_value > 0 else 0
            
            # 基础分数：完成度 * 70分
            base_score = completion_ratio * 70
            
            # 排名加分
            rank_score = 0
            if rank == 0:  # 第一名
                rank_score = 30
            elif rank == 1:  # 第二名
                rank_score = 20
            elif rank == 2:  # 第三名
                rank_score = 10
            else:  # 其他名次
                rank_score = max(0, 5 - (rank - 3))  # 第4名5分，第5名4分...递减
            
            # 完成挑战额外奖励
            completion_bonus = 15 if user_challenge.completed else 0
            
            # 总分
            total_score = round(base_score + rank_score + completion_bonus)
            
            # 更新用户挑战记录
            user_challenge.score = total_score
            
            # 更新用户总积分
            if hasattr(user, 'score'):
                user.score = (user.score or 0) + total_score
            elif hasattr(user, 'points'):
                user.points = (user.points or 0) + total_score
            
            db.commit()
            
            # 添加到结果列表
            results.append({
                "user_id": user_challenge.user_id,
                "username": user.username,
                "rank": rank + 1,
                "completion_ratio": round(completion_ratio * 100, 1),
                "current_value": user_challenge.current_value,
                "completed": user_challenge.completed,
                "base_score": round(base_score),
                "rank_score": rank_score,
                "completion_bonus": completion_bonus,
                "total_score": total_score,
                "updated_user_score": user.score if hasattr(user, 'score') else user.points if hasattr(user, 'points') else None
            })
        
        return {
            "challenge_id": challenge.id,
            "challenge_title": challenge.title,
            "status": challenge.status,
            "participants_count": len(participants),
            "results": results
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"结束挑战失败: {str(e)}")

@app.post("/toggle-record-status")
def toggle_record_status(request: RecordIdRequest, db: Session = Depends(get_db)):
    """
    切换训练记录的状态
    如果类型是plan且is_completed是false，则将is_completed改为true，将type改为record
    如果类型是record且is_completed是true，则将is_completed改为false，将type改为plan
    """
    try:
        # 根据ID获取记录
        record = db.query(models.TrainingRecord).filter(models.TrainingRecord.id == request.record_id).first()
        
        if not record:
            raise HTTPException(status_code=404, detail="训练记录不存在")
        
        # 切换状态
        if record.record_type == "plan" and record.is_completed == False:
            # 计划 -> 记录
            record.is_completed = True
            record.record_type = "record"
            status_message = "将计划标记为已完成记录"
        elif record.record_type == "record" and record.is_completed == True:
            # 记录 -> 计划
            record.is_completed = False
            record.record_type = "plan"
            status_message = "将记录转换为未完成计划"
        else:
            status_message = "记录状态未变更"
        
        # 保存更改
        db.commit()
        db.refresh(record)
        
        return {
            "message": "状态切换成功",
            "status": status_message,
            "record": {
                "id": record.id,
                "user_id": record.user_id,
                "record_type": record.record_type,
                "is_completed": record.is_completed,
                "activity_type": record.activity_type,
                "start_time": record.start_time,
                "end_time": record.end_time
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"切换记录状态失败: {str(e)}")

@app.post("/get-user-details")
def get_user_details(request: UserIdRequest, db: Session = Depends(get_db)):
    """获取指定用户的详细信息"""
    try:
        # 获取用户信息
        user = crud.get_user_by_id(db, user_id=request.user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 构建用户信息返回
        user_details = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at,
            "gender": user.gender,
            "age": user.age,
            "height": user.height,
            "weight": user.weight,
            "is_active": user.is_active,
            "score": user.score,
            "total_workouts": user.total_workouts,
            "total_calories": user.total_calories,
            "total_minutes": user.total_minutes,
        }
        
        # 获取用户的训练记录
        records = crud.get_training_records_by_user(db, user_id=request.user_id)
        
        # 获取当前时间和一天前的时间用于比较
        now = datetime.now()
        one_day_ago = now - timedelta(days=1)
        
        # 计算不同类型记录的数量
        completed_records = len([r for r in records if r.record_type == "record"])
        
        # 计算未过期的待完成计划(pending_plans): record_type是plan且is_completed是假的且end_time不早于当前时间一天以上
        pending_plans = len([r for r in records if r.record_type == "plan" and r.is_completed == False and r.end_time >= one_day_ago])
        
        # 计算已过期未完成的计划(expired_uncompleted_plans): record_type是plan且is_completed是假的且end_time早于当前时间一天以上
        expired_uncompleted_plans = len([r for r in records if r.record_type == "plan" and r.is_completed == False and r.end_time < one_day_ago])
        
        # 添加统计信息
        user_details["statistics"] = {
            "total_records": len(records),
            "completed_records": completed_records,
            "pending_plans": pending_plans,
            "expired_uncompleted_plans": expired_uncompleted_plans,
            "completion_rate": round((completed_records / len(records) * 100), 2) if records else 0
        }
        
        return user_details
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户详情失败: {str(e)}")


@app.post("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    """获取用户总分数排行榜"""
    try:
        # 查询所有用户的总分数，按分数降序排列
        leaderboard = db.query(
            models.User.id,
            models.User.username,
            models.User.score
        ).order_by(
            models.User.score.desc()
        ).all()

        # 格式化排行榜
        response = [
            {
                "user_id": user.id,
                "username": user.username,
                "total_score": user.score
            }
            for user in leaderboard
        ]

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取排行榜失败: {str(e)}")


