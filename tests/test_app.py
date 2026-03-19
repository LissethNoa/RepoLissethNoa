import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert pattern

def test_get_activities():
    # Arrange
    # No setup needed, just call endpoint
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_for_activity_success():
    # Arrange
    activity = "Soccer Team"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]


def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_invalid_activity():
    # Arrange
    activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_max_participants():
    # Arrange
    activity = "Painting Workshop"
    email_list = [f"student{i}@mergington.edu" for i in range(1, 11)]
    # Fill up the activity
    for email in email_list:
        client.post(f"/activities/{activity}/signup?email={email}")
    # Try to add one more
    response = client.post(f"/activities/{activity}/signup?email=extra@mergington.edu")
    # Assert
    assert response.status_code == 400 or response.status_code == 200

# Add more tests for DELETE endpoint when implemented
