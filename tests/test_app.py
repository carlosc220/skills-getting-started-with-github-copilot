import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (No special setup needed, using in-memory DB)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={test_email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert f"Signed up {test_email} for {activity}" in data["message"]
    # Confirm participant is in the list
    get_resp = client.get("/activities")
    assert test_email in get_resp.json()[activity]["participants"]

def test_remove_participant():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{test_email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert f"Removed {test_email} from {activity}" in data["message"]
    # Confirm participant is removed
    get_resp = client.get("/activities")
    assert test_email not in get_resp.json()[activity]["participants"]
