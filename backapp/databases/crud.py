from sqlalchemy.orm import Session
from backapp.databases import models
from datetime import datetime
from sqlalchemy import func, desc

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# 用户相关操作
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, username: str, email: str, password: str):
    db_user = models.User(username=username, email=email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_training_record(db: Session,
        filename: str,
        user_id: int,
        start_time: datetime,
        end_time: datetime,
        activity_type: str,
        duration_minutes: int,
):
    """创建新的训练记录"""
    db_record = models.TrainingRecord(
        filename=filename,
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        activity_type=activity_type,
        duration_minutes=duration_minutes
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def create_training_task(db: Session, 
                         user_id: int, 
                         task_name: str,
                         start_time: datetime,
                         end_time: datetime):
    """创建新的训练任务"""
    db_task = models.TrainingTask(
        user_id=user_id,
        task_name=task_name,
        start_time=start_time,
        end_time=end_time
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_training_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """获取该用户的所有训练任务"""
    return db.query(models.TrainingTask).filter(
        models.TrainingTask.user_id == user_id
    ).offset(skip).limit(limit).all()

def get_training_task(db: Session, task_id: int):
    """获取指定的训练任务"""
    return db.query(models.TrainingTask).filter(models.TrainingTask.id == task_id).first()

def update_training_task(db: Session, task_id: int, task_data: dict):
    """更新训练任务信息"""
    db_task = db.query(models.TrainingTask).filter(models.TrainingTask.id == task_id).first()
    if db_task:
        for key, value in task_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task
def delete_training_task(db: Session, task_id: int):
    """删除指定的训练任务"""
    db_task = db.query(models.TrainingTask).filter(models.TrainingTask.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False

def get_training_records_by_user(db: Session, user_id: int):
    """获取指定用户的所有训练记录"""
    return db.query(models.TrainingRecord).filter(
        models.TrainingRecord.user_id == user_id
    ).all()

def delete_training_record(db: Session, filename: str):
    """删除指定的训练记录"""
    db_record = db.query(models.TrainingRecord).filter(models.TrainingRecord.filename == filename).first()
    if db_record:
        db.delete(db_record)
        db.commit()
        return True
    return False

def update_training_record(db: Session, filename: str, record_data: dict):
    """更新训练记录信息"""
    db_record = db.query(models.TrainingRecord).filter(models.TrainingRecord.filename == filename).first()
    if db_record:
        for key, value in record_data.items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
        return db_record
    return None

def get_training_records_by_date_range(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    """获取用户在指定日期范围内的训练记录"""
    return db.query(models.TrainingRecord).filter(
        models.TrainingRecord.user_id == user_id,
        models.TrainingRecord.start_time >= start_date,
        models.TrainingRecord.start_time <= end_date
    ).all()

def get_training_records_by_date(db: Session, user_id: int, date: datetime):
    """获取用户在指定日期的训练记录"""
    start_datetime = datetime.combine(date, datetime.min.time())
    end_datetime = datetime.combine(date, datetime.max.time())
    
    return db.query(models.TrainingRecord).filter(
        models.TrainingRecord.user_id == user_id,
        models.TrainingRecord.start_time >= start_datetime,
        models.TrainingRecord.start_time <= end_datetime
    ).all()





# 健身房相关操作
def get_gyms(db: Session, skip: int = 0, limit: int = 100):
    """获取所有健身房"""
    return db.query(models.Gym).offset(skip).limit(limit).all()

def recommend_gyms_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    """为用户推荐健身房
    
    基于用户的历史预约记录、个人信息和健身房特点，为用户推荐最适合的健身房。
    推荐逻辑包括：
    1. 用户历史预约过的健身房
    2. 用户预约过的课程所属的健身房
    3. 受欢迎程度（预约人数多的健身房）
    4. 根据用户年龄和性别的个性化推荐
    """
    # 获取用户信息
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return []
    
    # 1. 获取用户历史预约过的健身房ID列表
    user_gym_ids = db.query(models.GymReservation.gym_id).filter(
        models.GymReservation.user_id == user_id,
        models.GymReservation.status == "confirmed"
    ).distinct().all()
    user_gym_ids = [gym_id for (gym_id,) in user_gym_ids]
    
    # 2. 获取用户预约过的课程所属的健身房ID列表
    course_gym_ids = db.query(models.GymCourse.gym_id).join(
        models.CourseReservation,
        models.CourseReservation.course_id == models.GymCourse.id
    ).filter(
        models.CourseReservation.user_id == user_id,
        models.CourseReservation.status == "confirmed"
    ).distinct().all()
    course_gym_ids = [gym_id for (gym_id,) in course_gym_ids]
    
    # 合并用户直接预约和通过课程预约的健身房ID
    preferred_gym_ids = list(set(user_gym_ids + course_gym_ids))
    
    # 3. 获取受欢迎的健身房（按预约人数排序）
    popular_gyms_query = db.query(
        models.Gym,
        func.count(models.GymReservation.id).label('reservation_count')
    ).outerjoin(
        models.GymReservation,
        models.GymReservation.gym_id == models.Gym.id
    ).group_by(models.Gym.id).order_by(desc('reservation_count'))
    
    # 4. 根据用户年龄和性别进行个性化推荐
    # 这里可以添加更复杂的推荐逻辑，例如根据用户年龄段和性别推荐不同类型的健身房
    
    # 构建最终的推荐结果
    # 首先添加用户历史偏好的健身房
    recommended_gyms = []
    if preferred_gym_ids:
        preferred_gyms = db.query(models.Gym).filter(
            models.Gym.id.in_(preferred_gym_ids)
        ).all()
        recommended_gyms.extend(preferred_gyms)
    
    # 然后添加受欢迎的健身房，但不重复添加已经在推荐列表中的健身房
    popular_gyms = popular_gyms_query.all()
    for gym, _ in popular_gyms:
        if gym.id not in [g.id for g in recommended_gyms]:
            recommended_gyms.append(gym)
            if len(recommended_gyms) >= limit:
                break
    
    # 如果推荐数量不足，添加其他健身房
    if len(recommended_gyms) < limit:
        other_gyms = db.query(models.Gym).filter(
            ~models.Gym.id.in_([g.id for g in recommended_gyms])
        ).limit(limit - len(recommended_gyms)).all()
        recommended_gyms.extend(other_gyms)
    
    # 应用分页并返回结果
    return recommended_gyms[skip:skip+limit]

def get_gym(db: Session, gym_id: str):
    """获取指定健身房"""
    return db.query(models.Gym).filter(models.Gym.gym_id == gym_id).first()

# 健身房课程相关操作
def get_gym_courses(db: Session, gym_id: int, skip: int = 0, limit: int = 100):
    """获取指定健身房的所有课程"""
    return db.query(models.GymCourse).filter(
        models.GymCourse.gym_id == gym_id
    ).offset(skip).limit(limit).all()

def get_gym_course(db: Session, course_id: int):
    """获取指定课程"""
    return db.query(models.GymCourse).filter(models.GymCourse.id == course_id).first()

# 课程预约相关操作
def create_course_reservation(db: Session, user_id: int, course_id: int):
    """创建课程预约"""
    # 检查课程是否存在
    course = get_gym_course(db, course_id)
    if not course:
        return None
    
    # 检查是否已经预约过
    existing_reservation = db.query(models.CourseReservation).filter(
        models.CourseReservation.user_id == user_id,
        models.CourseReservation.course_id == course_id,
        models.CourseReservation.status == "confirmed"
    ).first()
    
    if existing_reservation:
        return existing_reservation
    
    # 检查课程是否已满
    if course.current_reservations >= course.capacity:
        return None
    
    # 创建预约
    db_reservation = models.CourseReservation(
        user_id=user_id,
        course_id=course_id
    )
    
    # 更新课程当前预约人数
    course.current_reservations += 1
    
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

# 健身房预约相关操作
def create_gym_reservation(db: Session, user_id: int, gym_id: int, reservation_date: datetime, start_time: datetime, end_time: datetime):
    """创建健身房预约"""
    # 检查健身房是否存在
    gym = db.query(models.Gym).filter(models.Gym.id == gym_id).first()
    if not gym:
        return None
    
    # 创建预约
    db_reservation = models.GymReservation(
        user_id=user_id,
        gym_id=gym_id,
        reservation_date=reservation_date,
        start_time=start_time,
        end_time=end_time
    )
    
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


