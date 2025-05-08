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
usage: I used the prompt "使用python写一个BaseModel，内容是username, email, password”", and 
directly copy the code from its response 
"""
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

class EditRecordRequest(BaseModel):
    filename: str
    content: str
    user_id: int

class WeeklyPlanRequest(BaseModel):
    user_id: int
    date_str: str  # 格式为"x月x日"

class DailyPlanRequest(BaseModel):
    user_id: int
    date_str: str  # 格式为"x月x日"

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

class CommentResponse(DTO):
    user_id: int
    user_name: str
    comment: str
    time: datetime


class PostResponse(DTO):
    user_id: int
    user_name: str
    content: str
    time: datetime
    img_list: Optional[List[dict]] = None
    comments: List[CommentResponse] = []


class PostCreateRequest(DTO):
    content: str
    # 形如 [{"img": "http://..."}, {"img": "..."}]
    img_list: Optional[List[dict]] = None


class CommentCreateRequest(DTO):
    post_id: int
    comment: str



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

@app.post("/edit-record")
def edit_record(data: EditRecordRequest, db: Session = Depends(get_db)):
    """
    编辑指定文件名的训练记录及其文件
    """
    try:
        # 1. 更新文件内容
        file_path = os.path.join(SAVE_DIR, data.filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"文件不存在: {data.filename}")
        
        # 保存新内容到文件
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data.content)
            
        # 2. 提取数据并更新数据库记录
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
        
        # 更新数据库记录
        record_data = {
            "user_id": data.user_id,
            "start_time": start_time if start_time else datetime.now(),
            "end_time": end_time if end_time else datetime.now(),
            "activity_type": activity_type if activity_type else "未知",
            "duration_minutes": duration_minutes if duration_minutes else 0
        }
        
        updated_record = crud.update_training_record(db=db, filename=data.filename, record_data=record_data)
        
        if updated_record:
            return {
                "message": "训练记录已成功更新", 
                "filename": data.filename,
                "status": "success"
            }
        else:
            raise HTTPException(status_code=404, detail="未找到数据库中的训练记录")
    
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

    records = crud.get_training_records_by_user(db, user_id=data.user_id)
    print(f"[summary] 获取到记录数: {len(records)}")

    total_minutes = sum([r.duration_minutes or 0 for r in records])
    total_calories_actual = sum([r.calories or 0 for r in records])
    average_heart_rates = [r.average_heart_rate for r in records if r.average_heart_rate]
    max_heart_rates = [r.max_heart_rate for r in records if r.max_heart_rate]

    print(f"[summary] 总训练时长: {total_minutes} 分钟")
    print(f"[summary] 实际卡路里总和: {total_calories_actual} kcal")

    user = crud.get_user_by_id(db, data.user_id)
    if not user:
        print("[summary] 用户不存在")
        raise HTTPException(status_code=404, detail="用户不存在")

    weight = user.weight or 60
    MET = 8
    total_calories_estimated = MET * weight * (total_minutes / 60)
    print(f"[summary] 估算卡路里: {total_calories_estimated} kcal")

    return {
        "total_minutes": total_minutes,
        "estimated_calories": round(total_calories_estimated, 2),
        "actual_calories": total_calories_actual,
        "average_heart_rate": int(sum(average_heart_rates)/len(average_heart_rates)) if average_heart_rates else None,
        "max_heart_rate": max(max_heart_rates) if max_heart_rates else None
    }


@app.post("/stats/weekly-trend")
def get_weekly_trend(data: UserIdRequest, db: Session = Depends(get_db)):
    print(f"[trend] 收到 user_id: {data.user_id}")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)
    print(f"[trend] 查询时间范围: {start_date.date()} 到 {end_date.date()}")

    records = crud.get_training_records_by_date_range(
        db, user_id=data.user_id, start_date=start_date, end_date=end_date)
    print(f"[trend] 获取到记录数: {len(records)}")

    trend = {}
    for i in range(7):
        day = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        trend[day] = {
            "duration_minutes": 0,
            "calories": 0,
            "avg_heart_rate": [],
            "max_heart_rate": []
        }

    for r in records:
        date_str = r.start_time.strftime("%Y-%m-%d")
        trend[date_str]["duration_minutes"] += r.duration_minutes or 0
        trend[date_str]["calories"] += r.calories or 0
        if r.average_heart_rate:
            trend[date_str]["avg_heart_rate"].append(r.average_heart_rate)
        if r.max_heart_rate:
            trend[date_str]["max_heart_rate"].append(r.max_heart_rate)

    # 平均和最大心率整理
    for day_data in trend.values():
        avg_list = day_data["avg_heart_rate"]
        max_list = day_data["max_heart_rate"]
        day_data["avg_heart_rate"] = int(sum(avg_list)/len(avg_list)) if avg_list else None
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


# 动态分享序列化工具
def _serialize_comment(c: models.PostComment) -> CommentResponse:
    return CommentResponse(
        user_id=c.user_id,
        user_name=c.user.username,
        comment=c.content,
        time=c.created_at,
    )


def _serialize_post(post: models.Post) -> PostResponse:
    img_list = [{"img": url} for url in (post.images or [])]
    # 评论按时间倒序
    comments_sorted = sorted(post.comments, key=lambda x: x.created_at, reverse=True)
    return PostResponse(
        user_id=post.user_id,
        user_name=post.author.username,
        content=post.content,
        time=post.created_at,
        img_list=img_list or None,
        comments=[_serialize_comment(c) for c in comments_sorted],
    )


def _get_post_with_relations(db: Session, post_id: int) -> models.Post:
    post = (
        db.query(models.Post)
        .options(
            joinedload(models.Post.comments).joinedload(models.PostComment.user),
            joinedload(models.Post.author),
        )
        .filter(models.Post.id == post_id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


# 动态分享 相关接口

@app.post("/posts", summary="发布动态", response_model=PostResponse)
def create_post_api(
    body: PostCreateRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    images = [d["img"] for d in body.img_list] if body.img_list else None
    db_post = crud.create_post(
        db=db,
        user_id=current_user.id,
        content=body.content,
        images=images,
    )
    post_full = _get_post_with_relations(db, db_post.id)
    return _serialize_post(post_full)


@app.get("/posts", summary="获取动态列表", response_model=list[PostResponse])
def list_posts_api(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    posts = (
        db.query(models.Post)
        .options(
            joinedload(models.Post.comments).joinedload(models.PostComment.user),
            joinedload(models.Post.author),
        )
        .order_by(models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [_serialize_post(p) for p in posts]


@app.post("/posts/{post_id}/comments", summary="发表评论", response_model=CommentResponse)
def add_comment_api(
    post_id: int,
    body: CommentCreateRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 确保动态存在
    _get_post_with_relations(db, post_id)
    db_comment = crud.add_comment(
        db=db,
        user_id=current_user.id,
        post_id=post_id,
        content=body.comment,
    )
    return _serialize_comment(db_comment)


@app.get("/posts/{post_id}/comments", summary="获取评论列表", response_model=list[CommentResponse])
def list_comments_api(
    post_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    post = _get_post_with_relations(db, post_id)
    comments = sorted(post.comments, key=lambda x: x.created_at, reverse=True)[skip : skip + limit]
    return [_serialize_comment(c) for c in comments]