from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backapp.main import app
import datetime
from datetime import datetime, timedelta
client = TestClient(app)

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