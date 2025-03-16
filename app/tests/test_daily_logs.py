import pytest
from datetime import datetime
from .utils import get_test_token, get_auth_headers

def test_create_daily_log(client, test_user):
    token = get_test_token(test_user.username)
    headers = get_auth_headers(token)
    
    log_data = {
        "overall_mood": 8,
        "notes": "Feeling good today!"
    }
    
    response = client.post(
        "/daily-logs/",
        json=log_data,
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["overall_mood"] == 8
    assert data["notes"] == "Feeling good today!"
    assert "id" in data
    assert data["user_id"] == test_user.id

def test_get_daily_logs(client, test_user, test_db):
    # Create a test log first
    token = get_test_token(test_user.username)
    headers = get_auth_headers(token)
    
    log_data = {
        "overall_mood": 7,
        "notes": "Test log"
    }
    
    client.post("/daily-logs/", json=log_data, headers=headers)
    
    # Now get all logs
    response = client.get("/daily-logs/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["overall_mood"] == 7
    assert data[0]["notes"] == "Test log"

def test_update_daily_log(client, test_user, test_db):
    # Create a test log first
    token = get_test_token(test_user.username)
    headers = get_auth_headers(token)
    
    create_response = client.post(
        "/daily-logs/",
        json={"overall_mood": 6, "notes": "Initial log"},
        headers=headers
    )
    log_id = create_response.json()["id"]
    
    # Update the log
    update_data = {
        "overall_mood": 9,
        "notes": "Updated notes"
    }
    
    response = client.put(
        f"/daily-logs/{log_id}",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["overall_mood"] == 9
    assert data["notes"] == "Updated notes"

def test_delete_daily_log(client, test_user, test_db):
    # Create a test log first
    token = get_test_token(test_user.username)
    headers = get_auth_headers(token)
    
    create_response = client.post(
        "/daily-logs/",
        json={"overall_mood": 5, "notes": "Log to delete"},
        headers=headers
    )
    log_id = create_response.json()["id"]
    
    # Delete the log
    response = client.delete(
        f"/daily-logs/{log_id}",
        headers=headers
    )
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(
        f"/daily-logs/{log_id}",
        headers=headers
    )
    assert get_response.status_code == 404