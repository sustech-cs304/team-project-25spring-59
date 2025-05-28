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


if __name__ == 'main':
    test_get_gyms()
