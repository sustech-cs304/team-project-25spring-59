from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backapp.main import app
import datetime
from datetime import datetime, timedelta
client = TestClient(app)



def test_create_post_without_image():
    response = client.post(
        "/posts",
        data={
            "user_id": 1,
            "content": "这是一个测试动态"
        }
    )
    assert response.status_code == 200

def test_add_comment_to_post():
    post_id = 1
    comment_payload = {
        "user_id": 1,
        "comment": "这是一条自动化测试的评论"
    }

    response = client.post(f"/posts/{post_id}/comments", json=comment_payload)
    assert response.status_code == 200


def test_like_comment():
    comment_id = 1  # 确保该评论存在
    payload = {"user_id": 1}

    response = client.post(f"/comments/{comment_id}/like", json=payload)
    assert response.status_code == 200
    assert response.json()["comment_id"] == comment_id
    assert response.json()["message"] == "点赞成功"

def test_unlike_comment():
    comment_id = 1
    payload = {"user_id": 1}

    response = client.post(f"/comments/{comment_id}/unlike", json=payload)
    assert response.status_code == 200
    assert response.json()["comment_id"] == comment_id
    assert response.json()["message"] == "取消点赞成功"

# ------- 帖子点赞相关 --------

def test_like_post():
    post_id = 1  # 确保该帖子存在
    payload = {"user_id": 1}

    response = client.post(f"/posts/{post_id}/like", json=payload)
    assert response.status_code == 200
    assert response.json()["post_id"] == post_id
    assert response.json()["message"] == "点赞成功"

def test_unlike_post():
    post_id = 1
    payload = {"user_id": 1}

    response = client.post(f"/posts/{post_id}/unlike", json=payload)
    assert response.status_code == 200
    assert response.json()["post_id"] == post_id
    assert response.json()["message"] == "取消点赞成功"

# ------- 评论列表 --------

def test_get_post_comments():
    post_id = 1
    response = client.get(f"/posts/{post_id}/comments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)