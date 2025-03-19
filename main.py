import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# 定义文件存储路径
SAVE_DIR = "./TrainMission/posts"
# 确保目录存在
os.makedirs(SAVE_DIR, exist_ok=True)

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


# 登录接口
@app.post("/login")
def login(user: LoginRequest):
    print(f"Received login request: {user.username}, {user.password}")  # 这行代码可以帮助我们调试

    if user.username in fake_users_db and fake_users_db[user.username]["password"] == user.password:
        return {"message": "登录成功", "token": "mock-token"}

    raise HTTPException(status_code=401, detail="用户名或密码错误")


# 注册接口
@app.post("/register")
def register(user: RegisterRequest):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="用户名已存在")

    fake_users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "password": user.password  # 生产环境应存储加密密码
    }

    return {"message": "注册成功", "username": user.username}


@app.post("/saveMission")
def save_mission(data: SaveMissionRequest):
    try:
        file_path = os.path.join(SAVE_DIR, data.fileName)
        file_directory = os.path.dirname(file_path)

        # 确保目标目录存在
        os.makedirs(file_directory, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data.content)
        return {"message": "文件保存成功", "filePath": file_path, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": "文件保存失败", "error": str(e), "status": "failure"})