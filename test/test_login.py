from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backapp.main import app
import datetime
from datetime import datetime, timedelta
client = TestClient(app)

def test_register_success():
    # 构造注册请求 payload（使用一个唯一用户名和邮箱）
    register_payload = {
        "username": "new_test_user",
        "password": "testpassword123",
        "email": "new_test_user@example.com"
    }

    # 发送 POST 请求到注册接口
    response = client.post("/register", json=register_payload)

    # 打印响应状态码和内容便于调试
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 断言响应成功
    assert response.status_code == 200

    # 获取响应数据
    data = response.json()

    # 检查响应字段
    assert "message" in data and data["message"] == "注册成功"
    assert "username" in data and data["username"] == register_payload["username"]
def test_login_success():
    # 预注册一个用户（确保数据库里有这个用户）
    register_payload = {
        "username": "login_test_user",
        "password": "testpass123",
        "email": "login_test_user@example.com"
    }
    register_response = client.post("/register", json=register_payload)
    assert register_response.status_code == 200  # 忽略重复注册错误

    # 构造登录请求 payload
    login_payload = {
        "username": "login_test_user",
        "password": "testpass123"
    }

    # 发送 POST 请求
    response = client.post("/login", json=login_payload)

    # 打印响应状态码和 JSON，便于调试
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 断言响应成功
    assert response.status_code == 200

    # 获取响应数据
    data = response.json()

    # 检查响应字段
    assert "message" in data and data["message"] == "登录成功"
    assert "token" in data
    assert "user_id" in data
    assert "user" in data
    assert data["user"]["username"] == login_payload["username"]
    assert data["user"]["email"] == register_payload["email"]