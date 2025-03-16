# app/tests/test_entries.py
import pytest
from .utils import get_test_token, get_auth_headers

@pytest.fixture
def test_daily_log(client, test_user):
    token = get_test_token(test_user.username)
    headers = get_auth_headers(token)
    
    response = client.post(
        "/daily-logs/",
        json={"overall_mood": 7, "notes": "Test log for entries"},
        headers=headers
    )
    return response.json()

def test_create_food_entry(client, test_user, test_daily_log):
    token = get_test_token(test_user.username)
    headers = get_auth_headers(token)
    
    food_data = {
        "food_name": "Oatmeal",
        "meal_type": "breakfast",
        "calories": 300,
        "description": "With fruits and honey"
    }
    
    response = client.post(
        f"/daily-logs/{test_daily_log['id']}/food",
        json=food_data,
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["food_name"] == "Oatmeal"
    assert data["meal_type"] == "breakfast"
    assert data["calories"] == 300
    assert data["daily_log_id"] == test_daily_log["id"]

def test_create_exercise_entry(client, test_user, test_daily_log):
    token = get_test_token(test_user.username)
    headers = get_auth_headers(token)
    
    exercise_data = {
        "exercise_type": "Running",
        "duration_minutes": 30,
        "intensity": "moderate",
        "calories_burned": 250,
        "description": "Morning run in the park"
    }
    
    response = client.post(
        f"/daily-logs/{test_daily_log['id']}/exercise",
        json=exercise_data,
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["exercise_type"] == "Running"
    assert data["duration_minutes"] == 30
    assert data["intensity"] == "moderate"
    assert data["daily_log_id"] == test_daily_log["id"]

def test_get_food_entries(client, test_user, test_daily_log):
    token = get_test_token(test_user.username)
    headers = get_auth_headers(token)
    
    # Create a test food entry first
    food_data = {
        "food_name": "Salad",
        "meal_type": "lunch",
        "calories": 200
    }
    
    client.post(
        f"/daily-logs/{test_daily_log['id']}/food",
        json=food_data,
        headers=headers
    )
    
    # Get all food entries
    response = client.get(
        f"/daily-logs/{test_daily_log['id']}/food",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["food_name"] == "Salad"
    assert data[0]["meal_type"] == "lunch"