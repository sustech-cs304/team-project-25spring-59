from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, JSON, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum
from sqlalchemy.orm import relationship
# from .database import Base

Base = declarative_base()

# 用户-好友关联表（多对多）
friendship = Table(
    'friendships',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    gender = Column(String(10), nullable=True)
    age = Column(Integer, nullable=True)
    height = Column(Float, nullable=True)  
    weight = Column(Float, nullable=True) 
    is_active = Column(Boolean, default=True)

    # 统计信息
    total_workouts = Column(Integer, default=0)  # 总训练次数
    total_minutes = Column(Integer, default=0)  # 总训练时长(分钟)
    total_calories = Column(Integer, default=0)  # 总消耗卡路里
    score = Column(Integer, default=0)
    
    # 社交关系
    friends = relationship(
        "User", 
        secondary=friendship,
        primaryjoin=id==friendship.c.user_id,
        secondaryjoin=id==friendship.c.friend_id,
        backref="friend_of"
    )
    
    # 关系定义
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    challenge_participations = relationship("UserChallenge", back_populates="user", cascade="all, delete-orphan")

class TrainingRecord(Base):
    __tablename__ = "training_records"
    
    id = Column(Integer, primary_key=True, index=True)
    # # 外键关联用户表
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    
    # 基本训练信息
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    activity_type = Column(String(20), nullable=True)
    duration_minutes = Column(Integer, nullable=True)  # 运动时长(分钟)
    
    # 新增字段
    is_completed = Column(Boolean, default=False)  # 是否完成
    record_type = Column(String(10), default="record")  # "record"表示记录, "plan"表示计划
    
    # 提醒设置
    reminder_time = Column(DateTime, nullable=True)  # 提醒时间
    
    # 详细训练数据
    distance = Column(Float, nullable=True)  # 距离
    calories = Column(Integer, nullable=True)  # 卡路里
    average_heart_rate = Column(Integer, nullable=True)  # 平均心率
    max_heart_rate = Column(Integer, nullable=True)  # 最大心率
    # 每分钟心率数据，使用JSON格式存储
    # 格式: {"1": 120, "2": 125, "3": 130, ...} 表示第1分钟心率120，第2分钟心率125...
    minute_heart_rates = Column(JSON, nullable=True)

    # 关联用户
    user = relationship("User", backref="training_records")


class Gym(Base):
    """健身房表"""
    __tablename__ = "gyms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    open_time = Column(String(50), nullable=False)  # 格式如: "09:00:00-21:00:00"
    address = Column(String(200), nullable=False)
    
    # 关系定义 - 与课程表建立关联
    courses = relationship("GymCourse", back_populates="gym", cascade="all, delete-orphan")
    reservations = relationship("GymReservation", back_populates="gym", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Gym(id={self.id}, name={self.name})>"

class GymCourse(Base):
    """健身房课程表"""
    __tablename__ = "gym_courses"
    
    id = Column(Integer, primary_key=True, index=True)
    gym_id = Column(Integer, ForeignKey("gyms.id", ondelete="CASCADE"), nullable=False)
    course_name = Column(String(100), nullable=False)
    coach_name = Column(String(50), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False, default=20)  # 课程容量
    current_reservations = Column(Integer, nullable=False, default=0)  # 当前预约人数
    
    # 关系定义
    gym = relationship("Gym", back_populates="courses")
    reservations = relationship("CourseReservation", back_populates="course", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<GymCourse(id={self.id}, course_name={self.course_name}, gym_id={self.gym_id})>"

class CourseReservation(Base):
    """课程预约表"""
    __tablename__ = "course_reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("gym_courses.id", ondelete="CASCADE"), nullable=False)
    reservation_time = Column(DateTime, server_default=func.now())
    status = Column(String(20), nullable=False, default="confirmed")  # confirmed, cancelled
    
    # 关系定义
    user = relationship("User")
    course = relationship("GymCourse", back_populates="reservations")
    
    def __repr__(self):
        return f"<CourseReservation(id={self.id}, user_id={self.user_id}, course_id={self.course_id})>"

class GymReservation(Base):
    """健身房预约表"""
    __tablename__ = "gym_reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    gym_id = Column(Integer, ForeignKey("gyms.id", ondelete="CASCADE"), nullable=False)
    reservation_date = Column(DateTime, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default="confirmed")  # confirmed, cancelled
    
    # 关系定义
    user = relationship("User")
    gym = relationship("Gym", back_populates="reservations")
    
    def __repr__(self):
        return f"<GymReservation(id={self.id}, user_id={self.user_id}, gym_id={self.gym_id})>"

class Challenge(Base):
    """挑战表"""
    __tablename__ = "challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    challenge_type = Column(String(20), nullable=False)  # distance, calories, workouts, etc.
    target_value = Column(Float, nullable=False)  # 目标值
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    # 关系定义
    creator = relationship("User", backref="created_challenges")
    participants = relationship("UserChallenge", back_populates="challenge", cascade="all, delete-orphan")

class UserChallenge(Base):
    """用户参与挑战表"""
    __tablename__ = "user_challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False)
    join_date = Column(DateTime, server_default=func.now())
    current_value = Column(Float, default=0)  # 当前完成值
    completed = Column(Boolean, default=False)
    
    # 关系定义
    user = relationship("User", back_populates="challenge_participations")
    challenge = relationship("Challenge", back_populates="participants")

class Post(Base):
    """社交帖子表"""
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String(500), nullable=False)
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    
    # 可以关联到训练记录
    training_record_filename = Column(Integer, ForeignKey("training_records.id"), nullable=True)
    
    # 关系定义
    user = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    training_record = relationship("TrainingRecord", backref="posts")

class Like(Base):
    """点赞表"""
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # 关系定义
    user = relationship("User", backref="likes")
    post = relationship("Post", back_populates="likes")

class Comment(Base):
    """评论表"""
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    content = Column(String(300), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # 关系定义
    user = relationship("User", backref="comments")
    post = relationship("Post", back_populates="comments")
