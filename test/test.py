from fastapi.testclient import TestClient
import sys
import os

# from backapp.databases import models
from backapp.databases.database import SessionLocal
from backapp.databases.models import TrainingRecord

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backapp.main import app
import datetime
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

client = TestClient(app)


########################## 健身课程及预约相关api ###############################
def test_get_gyms():
    response = client.get("/gym/getGyms")
    assert response.status_code == 200

    gyms = response.json()
    assert isinstance(gyms, list)
    assert len(gyms) == 50
    expected = [
        {
            "name": "动享健身中心",
            "openTime": "06:00:00-23:00:00",
            "address": "深圳市宝安区新安街道创业二路123号星港同创汇3楼"
        },
        {
            "name": "动力时刻健身",
            "openTime": "06:00:00-23:00:00",
            "address": "深圳市坪山区坪山大道200号益田假日广场4楼"
        },
        {
            "name": "乐动力健身馆",
            "openTime": "08:00:00-22:00:00",
            "address": "深圳市宝安区新安街道创业二路123号星港同创汇3楼"
        },
    ]

    for i in range(3):
        assert gyms[i]["name"] == expected[i]["name"]
        assert gyms[i]["openTime"] == expected[i]["openTime"]
        assert gyms[i]["address"] == expected[i]["address"]


def test_get_courses():
    gym_id = 1
    response = client.get(f"/gym/getCourses/{gym_id}")
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) == 2

    expected = [
        {
            "id": 56,
            "gymId": 1,
            "courseName": "高强度间歇训练",
            "coachName": "王刚(CrossFit L2认证教练)",
            "startTime": "2025-06-01 06:48:32",
            "endTime": "2025-06-01 07:48:32",
            "capacity": 12,
            "currentReservations": 0
        },
        {
            "id": 74,
            "gymId": 1,
            "courseName": "功能性训练",
            "coachName": "张伟(ACSM认证教练)",
            "startTime": "2025-05-28 06:48:32",
            "endTime": "2025-05-28 07:48:32",
            "capacity": 15,
            "currentReservations": 0
        }
    ]

    for i in range(2):
        assert courses[i]["id"] == expected[i]["id"]
        assert courses[i]["gymId"] == expected[i]["gymId"]
        assert courses[i]["courseName"] == expected[i]["courseName"]
        assert courses[i]["coachName"] == expected[i]["coachName"]
        assert courses[i]["startTime"] == expected[i]["startTime"]
        assert courses[i]["endTime"] == expected[i]["endTime"]
        assert courses[i]["capacity"] == expected[i]["capacity"]
        assert courses[i]["currentReservations"] == expected[i]["currentReservations"]

def test_reserve_course_falied_alreadyReserved():
    payload = {
        "user_id": 1,
        "course_id": 1
    }
    response = client.post("/gym/reserveCourse", json=payload)
    assert response.status_code == 400

def test_reserve_course_failed_capcityOverflowed():
    payload = {
        "user_id": 1,
        "course_id": 6
    }
    response = client.post("/gym/reserveCourse", json=payload)
    assert response.status_code == 400

def test_reserve_course_successfully():
    payload = {
        "user_id": 1,
        "course_id": 12
    }
    response = client.post("/gym/reserveCourse", json=payload)
    assert response.status_code == 200

def test_cancel_course_reservation():
    payload = {
        "user_id": 1,
        "course_id": 12
    }
    response = client.post("/gym/cancelCourseReservation", json=payload)
    assert response.status_code == 200



def test_get_reserved_courses():
    user_id = 1
    response = client.get(f"/course/getReservedCourses/{user_id}")
    assert response.status_code == 200

    reservations = response.json()
    assert isinstance(reservations, list)

    expected = [
        {"courseId": 1, "gymId": 3},
        {"courseId": 3, "gymId": 29},
        {"courseId": 19, "gymId": 27},
    ]

    for i in range(len(expected)):
        assert reservations[i]["courseId"] == expected[i]["courseId"]
        assert reservations[i]["gymId"] == expected[i]["gymId"]


def test_save_mission():
    start_time = datetime.now().isoformat()
    end_time = (datetime.now() + timedelta(minutes=45)).isoformat()

    payload = {
        "user_id": 1,
        "start_time": start_time,
        "end_time": end_time,
        "activity_type": "cycling",
        "duration_minutes": 45,
        "calories": 300,
        "average_heart_rate": 130,
        "is_completed": True
    }

    response = client.post("/saveMission", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_edit_record():
    payload = {
        "record_id": 1,
        "user_id": 1,
        "activity_type": "running",
        "duration_minutes": 60
    }

    response = client.post("/edit-record", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["record_id"] == 1

def test_delete_record_failed():
    payload = {
        "record_id": 20000000
    }

    response = client.post("/delete-record", json=payload)

    assert response.status_code in [500, 404]



def test_get_daily_plan():
    payload = {
        "user_id": 10,
        "date_str": "2025年9月30日"
    }

    response = client.post("/get-daily-plan", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "date" in data
    assert "full_date" in data
    assert "training_items" in data
    assert isinstance(data["training_items"], list)

    assert data["date"] == "2025年9月30日"
def test_delete_record_success():
    payload = {
        "record_id": 1
    }

    response = client.post("/delete-record", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "训练记录已成功删除"
    assert data["record_id"] == 1
def test_edit_record_success():
    payload = {
        "record_id": 4,
        "user_id": 1,
        "activity_type": "running",
        "duration_minutes": 60
    }

    response = client.post("/edit-record", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "训练记录已成功更新"
    assert data["record_id"] == 4
    assert data["record_type"] == "record"
    assert data["status"] == "success"
def test_get_weekly_plan_success():
    payload = {
        "user_id": 1,
        "date_str": "5月10日"
    }

    response = client.post("/get-weekly-plan", json=payload)

    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 200
    data = response.json()
    assert "week_start" in data
    assert "week_end" in data
    assert "weekTasks" in data
    assert len(data["weekTasks"]) == 7
    for task in data["weekTasks"]:
        assert "title" in task
        assert "date" in task
        assert "tasks" in task
def test_get_training_summary_success():
    # 构造请求所需的 payload 数据
    payload = {
        "user_id": 1
    }

    # 发送 POST 请求到 /stats/summary 接口
    response = client.post("/stats/summary", json=payload)

    # 打印响应状态码和响应的 JSON 数据，方便调试
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 断言响应状态码为 200，表示请求成功
    assert response.status_code == 200

    # 获取响应的 JSON 数据
    data = response.json()

    # 断言返回的数据中包含预期的字段
    assert "total_minutes" in data
    assert "estimated_calories" in data
    assert "actual_calories" in data
    assert "average_heart_rate" in data
    assert "max_heart_rate" in data

    # 可以根据实际情况添加更多的断言，例如检查数据类型等
    assert isinstance(data["total_minutes"], int) or isinstance(data["total_minutes"], float)
    assert isinstance(data["estimated_calories"], int) or isinstance(data["estimated_calories"], float)
    assert isinstance(data["actual_calories"], int) or isinstance(data["actual_calories"], float)
    if data["average_heart_rate"] is not None:
        assert isinstance(data["average_heart_rate"], int)
    if data["max_heart_rate"] is not None:
        assert isinstance(data["max_heart_rate"], int)
def test_get_weekly_trend_success():
    # 构造请求所需的 payload 数据
    payload = {
        "user_id": 1
    }
    start_date = "2024-01-01"
    end_date = "2024-01-07"

    # 发送 POST 请求到 /stats/weekly-trend 接口
    response = client.post(f"/stats/weekly-trend?start_date={start_date}&end_date={end_date}", json=payload)

    # 打印响应状态码和响应的 JSON 数据，方便调试
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 断言响应状态码为 200，表示请求成功
    assert response.status_code == 200

    # 获取响应的 JSON 数据
    data = response.json()

    # 计算日期范围的天数
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    days = (end - start).days + 1

    # 断言返回的数据长度符合日期范围
    assert len(data) == days

    # 遍历每一天的数据，检查字段和数据类型
    for date_str, day_data in data.items():
        assert isinstance(date_str, str)
        assert isinstance(day_data, dict)
        assert "duration_minutes" in day_data
        assert "calories" in day_data
        assert "avg_heart_rate" in day_data
        assert "max_heart_rate" in day_data

        assert isinstance(day_data["duration_minutes"], int)
        assert isinstance(day_data["calories"], int)
        if day_data["avg_heart_rate"] is not None:
            assert isinstance(day_data["avg_heart_rate"], int)
        if day_data["max_heart_rate"] is not None:
            assert isinstance(day_data["max_heart_rate"], int)
def test_get_weekly_trend_invalid_date_format():
    # 构造请求所需的 payload 数据
    payload = {
        "user_id": 1
    }
    start_date = "2024/01/01"  # 错误的日期格式
    end_date = "2024/01/07"

    # 发送 POST 请求到 /stats/weekly-trend 接口
    response = client.post(f"/stats/weekly-trend?start_date={start_date}&end_date={end_date}", json=payload)

    # 打印响应状态码和响应的 JSON 数据，方便调试
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 断言响应状态码为 400，表示日期格式错误
    assert response.status_code == 400

    # 断言响应的错误信息包含预期内容
    data = response.json()
    assert "日期格式错误，应为 YYYY-MM-DD" in data.get("detail", "")

def test_create_challenge_success():
    # 构造请求 payload
    payload = {
        "title": "测试挑战",
        "description": "测试挑战描述",
        "start_date": "2025-06-01T00:00:00",
        "end_date": "2025-06-10T00:00:00",
        "challenge_type": "calories",
        "target_value": 5000,
        "created_by": 1
    }

    # 发送 POST 请求
    response = client.post("/challenges", json=payload)

    # 打印响应状态码和响应 JSON，便于调试
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 断言响应成功
    assert response.status_code == 200

    # 获取响应数据
    data = response.json()

    # 检查响应字段和数据类型
    assert "id" in data
    assert "title" in data and data["title"] == payload["title"]
    assert "description" in data and data["description"] == payload["description"]
    assert "start_date" in data and data["start_date"].startswith("2025-06-01")
    assert "end_date" in data and data["end_date"].startswith("2025-06-10")
    assert "challenge_type" in data and data["challenge_type"] == payload["challenge_type"]
    assert "target_value" in data and data["target_value"] == payload["target_value"]
    assert "created_by" in data and data["created_by"] == payload["created_by"]
def test_join_challenge_success():
    # 预先创建一个挑战（你可以直接调用接口或通过 db fixture 预置数据）
    challenge_payload = {
        "title": "加入挑战测试",
        "description": "这是一个用于测试加入挑战的挑战",
        "start_date": "2025-06-01T00:00:00",
        "end_date": "2025-06-10T00:00:00",
        "challenge_type": "calories",
        "target_value": 3000,
        "created_by": 1
    }
    create_response = client.post("/challenges", json=challenge_payload)
    assert create_response.status_code == 200
    challenge_id = create_response.json()["id"]

    # 构造加入挑战请求 payload
    join_payload = {
        "user_id": 1,
        "challenge_id": challenge_id
    }

    # 发送 POST 请求
    response = client.post("/challenges/join", json=join_payload)

    # 打印响应状态码和响应 JSON，便于调试
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 断言响应成功
    assert response.status_code == 200

    # 获取响应数据
    data = response.json()

    # 检查响应字段（根据你的 UserChallengeResponse 定义）
    assert "id" in data  # 加入记录的 id
    assert "user_id" in data and data["user_id"] == join_payload["user_id"]
    assert "challenge_id" in data and data["challenge_id"] == join_payload["challenge_id"]
    assert "join_date" in data  # 修改这里，原来是 "joined_at"
    assert "current_value" in data and data["current_value"] == 0.0
    assert "completed" in data and data["completed"] is False
def test_get_all_challenges_success():
    # 预先创建一个挑战
    challenge_payload = {
        "title": "测试获取挑战",
        "description": "这是用于测试获取所有挑战的挑战",
        "start_date": "2025-06-01T00:00:00",
        "end_date": "2025-06-10T00:00:00",
        "challenge_type": "steps",
        "target_value": 10000,
        "created_by": 1
    }
    create_response = client.post("/challenges", json=challenge_payload)
    assert create_response.status_code == 200
    created_challenge_id = create_response.json()["id"]

    # 发送 GET 请求获取所有挑战
    response = client.get("/challenges/all")

    # 打印响应状态码和 JSON 内容，便于调试
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 断言响应成功
    assert response.status_code == 200

    # 获取响应数据
    data = response.json()
    assert "challenges" in data
    assert "total_count" in data

    # 查找我们刚刚创建的挑战
    challenges = data["challenges"]
    matched = [ch for ch in challenges if ch["id"] == created_challenge_id]
    assert len(matched) == 1  # 确保找到了对应挑战

    challenge_data = matched[0]

    # 校验挑战字段（你可以根据具体返回字段再补充）
    assert challenge_data["title"] == challenge_payload["title"]
    assert challenge_data["description"] == challenge_payload["description"]
    assert challenge_data["challenge_type"] == challenge_payload["challenge_type"]
    assert challenge_data["target_value"] == challenge_payload["target_value"]
    assert challenge_data["created_by"] == challenge_payload["created_by"]
    assert "status" in challenge_data
    assert "participants_count" in challenge_data
    assert "completion_rate" in challenge_data
    assert "top_performers" in challenge_data
    assert isinstance(challenge_data["top_performers"], list)
    assert "days_remaining" in challenge_data
def test_update_challenge_progress_success():
    # 创建一个挑战
    challenge_payload = {
        "title": "测试进度更新",
        "description": "这是用于测试更新进度的挑战",
        "start_date": "2025-06-01T00:00:00",
        "end_date": "2025-06-10T00:00:00",
        "challenge_type": "calories",
        "target_value": 500,
        "created_by": 1
    }
    create_response = client.post("/challenges", json=challenge_payload)
    assert create_response.status_code == 200
    challenge_id = create_response.json()["id"]

    # 加入挑战
    join_payload = {
        "user_id": 1,
        "challenge_id": challenge_id
    }
    join_response = client.post("/challenges/join", json=join_payload)
    assert join_response.status_code == 200

    # 更新挑战进度
    update_payload = {
        "user_id": 1,
        "challenge_id": challenge_id,
        "current_value": 600  # 大于目标值，用于测试 completed == True
    }
    response = client.post("/challenges/update-progress", json=update_payload)

    # 打印调试信息
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 断言响应成功
    assert response.status_code == 200

    # 检查返回数据
    data = response.json()
    assert data["message"] == "进度已更新"
    assert data["current_value"] == update_payload["current_value"]
    assert data["completed"] is True  # 已达成目标
    assert "progress" in data
    assert data["progress"] == 100  # 超过目标值，进度应为 100%
def test_get_challenge_detail_success():
    # 创建一个挑战
    challenge_payload = {
        "title": "测试挑战详情",
        "description": "用于测试获取挑战详情接口",
        "start_date": "2025-06-01T00:00:00",
        "end_date": "2025-06-10T00:00:00",
        "challenge_type": "steps",
        "target_value": 10000,
        "created_by": 1
    }
    create_response = client.post("/challenges", json=challenge_payload)
    assert create_response.status_code == 200
    challenge_id = create_response.json()["id"]

    # 用户加入挑战
    join_payload = {
        "user_id": 1,
        "challenge_id": challenge_id
    }
    join_response = client.post("/challenges/join", json=join_payload)
    assert join_response.status_code == 200

    # 更新用户进度（用于生成排行榜）
    progress_payload = {
        "user_id": 1,
        "challenge_id": challenge_id,
        "current_value": 5000
    }
    update_response = client.post("/challenges/update-progress", json=progress_payload)
    assert update_response.status_code == 200

    # 获取挑战详情
    detail_payload = {
        "challenge_id": challenge_id
    }
    response = client.post("/challenges/detail", json=detail_payload)

    # 打印调试信息
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 断言响应成功
    assert response.status_code == 200
    data = response.json()

    # 校验 challenge 字段
    challenge = data["challenge"]
    assert challenge["id"] == challenge_id
    assert challenge["title"] == challenge_payload["title"]
    assert challenge["description"] == challenge_payload["description"]
    assert challenge["challenge_type"] == challenge_payload["challenge_type"]
    assert challenge["target_value"] == challenge_payload["target_value"]
    assert challenge["created_by"] == challenge_payload["created_by"]
    assert "status" in challenge  # 状态可能是 ongoing、upcoming 等

    # 校验 participants_count
    assert data["participants_count"] == 1

    # 校验排行榜
    leaderboard = data["leaderboard"]
    assert isinstance(leaderboard, list)
    assert len(leaderboard) == 1

    top_entry = leaderboard[0]
    assert top_entry["user_id"] == 1
    assert "username" in top_entry  # 确保 join 中的 User 表字段也返回了
    assert top_entry["current_value"] == 5000
    assert top_entry["completed"] is False
    assert top_entry["progress"] == 50.0  # 5000 / 10000
def test_get_my_challenges_success():
    # 创建一个挑战
    challenge_payload = {
        "title": "测试我的挑战",
        "description": "用于测试获取用户参与的挑战",
        "start_date": "2025-06-01T00:00:00",
        "end_date": "2025-06-10T00:00:00",
        "challenge_type": "calories",
        "target_value": 300,
        "created_by": 1
    }
    create_response = client.post("/challenges", json=challenge_payload)
    assert create_response.status_code == 200
    challenge_id = create_response.json()["id"]

    # 用户加入该挑战
    join_payload = {
        "user_id": 1,
        "challenge_id": challenge_id
    }
    join_response = client.post("/challenges/join", json=join_payload)
    assert join_response.status_code == 200

    # 请求获取该用户参与的挑战列表
    request_payload = {
        "user_id": 1
    }
    response = client.post("/challenges/my", json=request_payload)

    # 打印调试信息
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 断言响应成功
    assert response.status_code == 200
    challenges = response.json()
    assert isinstance(challenges, list)

    # 查找是否包含刚创建的挑战
    matched = [ch for ch in challenges if ch["id"] == challenge_id]
    assert len(matched) == 1  # 确保用户参与的挑战中包含该挑战

    challenge_data = matched[0]

    # 校验挑战基本字段
    assert challenge_data["id"] == challenge_id
    assert challenge_data["title"] == challenge_payload["title"]
    assert challenge_data["description"] == challenge_payload["description"]
    assert challenge_data["challenge_type"] == challenge_payload["challenge_type"]
    assert challenge_data["target_value"] == challenge_payload["target_value"]
    assert challenge_data["created_by"]== challenge_payload["created_by"]
    assert "start_date" in challenge_data
    assert "end_date" in challenge_data
def test_end_challenge_success():
    # 1. 创建一个新的挑战
    challenge_payload = {
        "title": "测试结束挑战",
        "description": "用于测试挑战结束及得分计算",
        "start_date": "2025-06-01T00:00:00",
        "end_date": "2025-06-10T00:00:00",
        "challenge_type": "steps",
        "target_value": 10000,
        "created_by": 1  # 假设用户1存在
    }
    create_response = client.post("/challenges", json=challenge_payload)
    assert create_response.status_code == 200
    challenge_id = create_response.json()["id"]

    # 2. 用户加入挑战（可以多次加入模拟多个用户参与）
    for i in range(1, 4):  # 假设用户1、2、3都存在
        join_payload = {
            "user_id": i,
            "challenge_id": challenge_id
        }
        join_response = client.post("/challenges/join", json=join_payload)
        assert join_response.status_code == 200

        # 同时模拟用户完成情况
        update_payload = {
            "user_id": i,
            "challenge_id": challenge_id,
            "current_value": 6000 + i * 1000,  # 模拟完成值不同
            "completed": (i % 2 == 1)  # 用户1和3完成挑战
        }
        update_response = client.post("/challenges/update-progress", json=update_payload)
        assert update_response.status_code == 200

    # 3. 调用结束挑战接口
    end_payload = {
        "challenge_id": challenge_id
    }
    response = client.post("/challenges/end", json=end_payload)

    # 打印调试信息
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 4. 验证接口调用成功
    assert response.status_code == 200
    data = response.json()
    assert data["challenge_id"] == challenge_id
    assert data["status"] == "已结束"
    assert "results" in data
    assert isinstance(data["results"], list)
    assert len(data["results"]) >= 1

    # 5. 验证结果字段完整
    for result in data["results"]:
        assert "user_id" in result
        assert "username" in result
        assert "rank" in result
        assert "completion_ratio" in result
        assert "current_value" in result
        assert "completed" in result
        assert "base_score" in result
        assert "rank_score" in result
        assert "completion_bonus" in result
        assert "total_score" in result
        assert "updated_user_score" in result


def test_get_leaderboard_success():
    # 预置一些用户数据（如果没有数据库 fixture，这里假设用户和积分已存在）
    # 否则你可以使用数据库直接插入或依赖已有的测试数据

    # 示例：可选创建用户数据（你也可以在数据库中用 fixture 创建）
    # 这里假设用户表中已存在以下数据：
    # 用户1：score=120
    # 用户2：score=150
    # 用户3：score=90

    # 发送 GET 请求到排行榜接口（你定义的是 POST）
    response = client.post("/leaderboard")

    # 打印状态码和响应内容方便调试
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    # 断言状态码正确
    assert response.status_code == 200

    # 获取响应数据
    data = response.json()

    # 断言返回是列表
    assert isinstance(data, list)
    assert len(data) >= 1  # 至少返回一个用户，除非你测试环境是空的

    # 检查字段结构
    for entry in data:
        assert "user_id" in entry
        assert "username" in entry
        assert "total_score" in entry

    # 可选：断言按 total_score 降序排列
    scores = [user["total_score"] for user in data]
    assert scores == sorted(scores, reverse=True)
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









if __name__ == 'main':
    test_get_gyms()