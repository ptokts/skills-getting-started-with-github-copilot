import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange
    # No special setup needed - activities are predefined in app
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Verify structure
    chess = data["Chess Club"]
    assert "description" in chess
    assert "schedule" in chess
    assert "max_participants" in chess
    assert "participants" in chess

def test_signup_success():
    # Arrange
    activity_name = "Basketball Team"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {email} for {activity_name}"
    
    # Verify added to activities
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity_name]["participants"]

def test_signup_activity_not_found():
    # Arrange
    invalid_activity = "NonExistent Activity"
    email = "test@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{invalid_activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_signup_already_signed_up():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"
    # Pre-signup the student
    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"

def test_unregister_success():
    # Arrange
    activity_name = "Programming Class"
    email = "remove@mergington.edu"
    # Pre-signup the student
    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Unregistered {email} from {activity_name}"
    
    # Verify removed from activities
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities[activity_name]["participants"]

def test_unregister_activity_not_found():
    # Arrange
    invalid_activity = "NonExistent Activity"
    email = "test@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{invalid_activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_unregister_not_signed_up():
    # Arrange
    activity_name = "Art Club"
    email = "notsigned@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student is not signed up for this activity"

def test_root_redirect():
    # Arrange
    # No special setup needed
    
    # Act
    response = client.get("/")
    
    # Assert
    assert response.status_code == 200  # TestClient follows redirects by default
    # The redirect leads to static file serving
