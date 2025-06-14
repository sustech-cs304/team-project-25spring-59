from sqlalchemy.orm import Session
from backapp.databases import models
from datetime import datetime
from sqlalchemy import func, desc
from typing import Optional 
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
        user_id: int,
        start_time: datetime,
        end_time: datetime,
        activity_type: str,
        duration_minutes: int,
        calories: Optional[int] = None ,
        average_heart_rate: Optional[int] = None,
        is_completed: bool = False
):
    """创建新的训练记录"""
    # 修复时区比较问题
    now = datetime.now()
    
    # 确保两个datetime对象都是naive的(不带时区)
    if start_time.tzinfo is not None:
        start_time = start_time.replace(tzinfo=None)
    
    record_type = "record" if start_time < now else "plan"
    
    db_record = models.TrainingRecord(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        activity_type=activity_type,
        duration_minutes=duration_minutes,
        calories=calories,
        average_heart_rate=average_heart_rate,
        is_completed=is_completed,
        record_type=record_type
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_training_records_by_user(db: Session, user_id: int):
    """获取指定用户的所有训练记录"""
    return db.query(models.TrainingRecord).filter(
        models.TrainingRecord.user_id == user_id
    ).all()

def delete_training_record(db: Session, record_id: int):
    """删除指定ID的训练记录"""
    db_record = db.query(models.TrainingRecord).filter(models.TrainingRecord.id == record_id).first()
    if db_record:
        db.delete(db_record)
        db.commit()
        return True
    return False

def update_training_record(db: Session, record_id: int, record_data: dict):
    """更新指定ID的训练记录信息"""
    db_record = db.query(models.TrainingRecord).filter(models.TrainingRecord.id == record_id).first()
    if db_record:
        # 当更新start_time时，需要更新record_type
        if 'start_time' in record_data:
            start_time = record_data['start_time']
            if start_time.tzinfo is not None:
                start_time = start_time.replace(tzinfo=None)
            now = datetime.now()
            record_data['record_type'] = "record" if start_time < now else "plan"
        
        # 更新记录字段
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

def create_challenge(db: Session,
                    title: str,
                    description: str,
                    start_date: datetime,
                    end_date: datetime,
                    challenge_type: str,
                    target_value: float,
                    created_by: int,
                    status: str):
    """创建新的挑战"""
    db_challenge = models.Challenge(
        title=title,
        description=description,
        start_date=start_date,
        end_date=end_date,
        challenge_type=challenge_type,
        target_value=target_value,
        created_by=created_by,
        status=status
    )
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    
    return db_challenge

def join_challenge(db: Session, user_id: int, challenge_id: int):
    """用户加入挑战"""
    # 检查是否已加入
    existing = db.query(models.UserChallenge).filter(
        models.UserChallenge.user_id == user_id,
        models.UserChallenge.challenge_id == challenge_id
    ).first()
    
    if existing:
        return existing
    
    # 创建新的参与记录
    user_challenge = models.UserChallenge(
        user_id=user_id,
        challenge_id=challenge_id,
        current_value=0,
        completed=False
    )
    db.add(user_challenge)
    db.commit()
    db.refresh(user_challenge)
    return user_challenge


# 健身房相关操作
def get_gyms(db: Session, skip: int = 0, limit: int = 100):
    """获取所有健身房"""
    return db.query(models.Gym).offset(skip).limit(limit).all()


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
        models.CourseReservation.course_id == course_id
    ).first()
    
    if existing_reservation:
        return None
    
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


# --------------------------------------
# 动态 / 分享（Post）相关 CRUD
# --------------------------------------

# Post
def create_post(
    db: Session,
    user_id: int,
    content: str
):
    db_post = models.Post(
        user_id=user_id,
        content=content
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post(db: Session, post_id: int):
    """获取指定动态"""
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 20):
    """按时间倒序获取动态列表"""
    return (
        db.query(models.Post)
        .order_by(models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_posts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 20):
    """获取某个用户发布的动态"""
    return (
        db.query(models.Post)
        .filter(models.Post.user_id == user_id)
        .order_by(models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_post(db: Session, post_id: int, update_data: dict):
    """更新动态"""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        for k, v in update_data.items():
            setattr(db_post, k, v)
        db.commit()
        db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    """删除动态"""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False


# Like
def like_post(db: Session, user_id: int, post_id: int):
    """点赞（若已点则返回现有记录）"""
    existing = (
        db.query(models.Like)
        .filter(
            models.Like.user_id == user_id,
            models.Like.post_id == post_id,
        )
        .first()
    )
    if existing:
        return existing

    db_like = models.Like(user_id=user_id, post_id=post_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def unlike_post(db: Session, user_id: int, post_id: int):
    """取消点赞"""
    like = (
        db.query(models.Like)
        .filter(
            models.Like.user_id == user_id,
            models.Like.post_id == post_id,
        )
        .first()
    )
    if like:
        db.delete(like)
        db.commit()
        return True
    return False


def count_post_likes(db: Session, post_id: int) -> int:
    """统计点赞数"""
    return db.query(models.Like).filter(models.Like.post_id == post_id).count()


# Comment
def add_comment(db: Session, user_id: int, post_id: int, content: str):
    """添加评论"""
    db_comment = models.Comment(
        user_id=user_id,
        post_id=post_id,
        content=content,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments(db: Session, post_id: int, skip: int = 0, limit: int = 50):
    """获取评论列表（倒序）"""
    return (
        db.query(models.Comment)
        .filter(models.Comment.post_id == post_id)
        .order_by(models.Comment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_comment(db: Session, comment_id: int):
    """删除评论"""
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
        return True
    return False


def count_post_comments(db: Session, post_id: int) -> int:
    """统计评论数"""
    return db.query(models.Comment).filter(models.Comment.post_id == post_id).count()

# like comment

def like_comment(db: Session, user_id: int, comment_id: int):
    existing = db.query(models.CommentLike).filter_by(user_id=user_id, comment_id=comment_id).first()
    if existing:
        return existing
    like = models.CommentLike(user_id=user_id, comment_id=comment_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

def unlike_comment(db: Session, user_id: int, comment_id: int):
    like = db.query(models.CommentLike).filter_by(user_id=user_id, comment_id=comment_id).first()
    if like:
        db.delete(like)
        db.commit()
        return True
    return False

def count_comment_likes(db: Session, comment_id: int) -> int:
    return db.query(models.CommentLike).filter_by(comment_id=comment_id).count()