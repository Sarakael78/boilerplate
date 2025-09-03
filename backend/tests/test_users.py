"""
Test cases for user endpoints.
"""
import pytest
from fastapi import status
from ..app.core.security import get_password_hash
from ..app.models.user import User


def test_create_user(test_client, test_db):
    """Test user creation endpoint."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    
    response = test_client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data


def test_create_user_duplicate_email(test_client, test_db):
    """Test user creation with duplicate email."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    
    # Create first user
    test_client.post("/api/v1/users/", json=user_data)
    
    # Try to create second user with same email
    response = test_client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_health_check(test_client):
    """Test health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "ok"
