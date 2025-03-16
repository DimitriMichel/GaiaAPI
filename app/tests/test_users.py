import pytest
from .utils import get_test_token, get_auth_headers

def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "newuser@example.com", "username": "newuser", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data

def test_read_users(client, test_user):
    token = get_test_token(test_user.username)
    headers = get_auth_headers(token)
    
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_read_user(client, test_user):
    token = get_test_token(test_user.username)
    headers = get_auth_headers(token)
    
    response = client.get(f"/users/{test_user.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user.username
    assert data["email"] == test_user.email

def test_read_user_unauthorized(client, test_user):
    # No authentication token
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 401

def test_read_nonexistent_user(client, test_user):
    token = get_test_token(test_user.username)
    headers = get_auth_headers(token)
    
    response = client.get("/users/999", headers=headers)
    assert response.status_code == 404