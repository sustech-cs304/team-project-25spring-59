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
from typing import Optional 


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
    insert_mock_data()  # 👈 启动时自动插入数据

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
    date_str: str  # 格式为"x月x日"

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
            
            # 计算挑战状态
            now = datetime.now()
            if now < challenge.start_date:
                status = "即将开始"
            elif now > challenge.end_date:
                status = "已结束"
            else:
                status = "进行中"
            
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
                "status": status,
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