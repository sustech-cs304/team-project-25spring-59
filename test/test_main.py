from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backapp.main import app
import datetime
from datetime import datetime, timedelta
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


def test_get_user_completed_records():
    payload = {
        "user_id": 1  
    }

    response = client.post("/generate-user-records/completed", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "records" in data
    assert "count" in data
    assert isinstance(data["records"], list)

    assert len(data) == 2
    if data["count"] > 0:
        record = data["records"][0]
        assert "id" in record
        assert "user_id" in record
        assert "start_time" in record
        assert "end_time" in record
        assert "activity_type" in record
        assert "duration_minutes" in record
        assert "is_completed" in record
        assert "record_type" in record


def test_get_user_missed_records():
    payload = {
        "user_id": 1  
    }

    response = client.post("/generate-user-records/missed-plans", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "records" in data
    assert "count" in data
    assert isinstance(data["records"], list)

    assert len(data) == 2
    if data["count"] > 0:
        record = data["records"][0]
        assert "id" in record
        assert "user_id" in record
        assert "start_time" in record
        assert "end_time" in record
        assert "activity_type" in record
        assert "duration_minutes" in record
        assert "is_completed" in record
        assert "record_type" in record


def test_get_user_upcoming_records():
    payload = {
        "user_id": 1  
    }

    response = client.post("/generate-user-records/upcoming-plans", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "records" in data
    assert "count" in data
    assert isinstance(data["records"], list)

    assert len(data) == 2
    if data["count"] > 0:
        record = data["records"][0]
        assert "id" in record
        assert "user_id" in record
        assert "start_time" in record
        assert "end_time" in record
        assert "activity_type" in record
        assert "duration_minutes" in record
        assert "is_completed" in record
        assert "record_type" in record



def test_toggle_record_status_successfully():
    record_id = 1

    response = client.post("/toggle-record-status", json={"record_id": record_id})
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "status" in data
    assert "record" in data
    assert data["record"]["id"] == record_id
    assert data["record"]["record_type"] in ["plan", "record"]
    assert isinstance(data["record"]["is_completed"], bool)

def test_toggle_record_status_failed():
    record_id = 114514

    response = client.post("/toggle-record-status", json={"record_id": record_id})
    assert response.status_code == 404


def test_get_user_successfully():
    user_id = 1

    response = client.post("/get-user-details", json={"user_id": user_id})
    assert response.status_code == 200

    data = response.json()
    
    # 基本字段断言
    assert data["id"] == user_id
    assert "username" in data
    assert "email" in data
    assert "created_at" in data
    assert "gender" in data
    assert "statistics" in data
    
    stats = data["statistics"]
    assert "total_records" in stats
    assert "completed_records" in stats
    assert "pending_plans" in stats
    assert "expired_uncompleted_plans" in stats
    assert "completion_rate" in stats

def test_get_user_failed():
    user_id = 114514

    response = client.post("/get-user-details", json={"user_id": user_id})
    assert response.status_code == 404



def test_get_in_progress_plans():
    user_id = 1  

    response = client.post("/generate-user-records/in-progress", json={"user_id": user_id})
    assert response.status_code == 200

    data = response.json()
    assert "records" in data
    assert "count" in data
    assert data["status"] == "正在进行中"

    for record in data["records"]:
        assert "id" in record
        assert "user_id" in record and record["user_id"] == user_id
        assert "start_time" in record
        assert "end_time" in record
        assert "record_type" in record and record["record_type"] == "plan"
        assert "is_completed" in record and record["is_completed"] is False

        now = datetime.now()
        start = datetime.fromisoformat(record["start_time"])
        end = datetime.fromisoformat(record["end_time"])
        assert start <= now <= end



def test_get_plans_starting_soon():
    user_id = 1  
    minutes = 600  

    response = client.post(
        "/generate-user-records/starting-soon",
        json={"user_id": user_id, "minutes": minutes}
    )
    
    assert response.status_code == 200

    data = response.json()
    assert "records" in data
    assert "count" in data
    assert "time_window" in data

    now = datetime.now()
    future = now + timedelta(minutes=minutes)

    for record in data["records"]:
        start_time = datetime.fromisoformat(record["start_time"])
        assert now <= start_time <= future
        assert record["record_type"] == "plan"
        assert record["is_completed"] is False
        assert record["user_id"] == user_id

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
if __name__ == 'main':
    test_get_gyms()
