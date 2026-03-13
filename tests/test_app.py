import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert: Test listing activities

def test_get_activities():
    # Arrange: None needed, app is ready
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Arrange-Act-Assert: Test signup for activity

def test_signup_for_activity():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Cleanup: Remove test user
    client.post(f"/activities/{activity}/unregister?email={email}")

# Arrange-Act-Assert: Test unregister for activity

def test_unregister_for_activity():
    # Arrange
    email = "testuser2@mergington.edu"
    activity = "Chess Club"
    # Add user first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"

# Arrange-Act-Assert: Test error on duplicate signup

def test_signup_duplicate():
    # Arrange
    email = "daniel@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

# Arrange-Act-Assert: Test error on unregistering non-participant

def test_unregister_nonparticipant():
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"
