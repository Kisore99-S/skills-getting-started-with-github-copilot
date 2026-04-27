from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange - No special setup needed
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "schedule" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_signup_success():
    # Arrange
    email = "test@mergington.edu"
    activity = "Basketball Team"  # Activity with no initial participants
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert f"Signed up {email} for {activity}" == result["message"]
    
    # Verify the participant was added
    response = client.get("/activities")
    data = response.json()
    assert email in data[activity]["participants"]


def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"  # Activity where michael is already signed up
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "already signed up" in result["detail"]


def test_signup_invalid_activity():
    # Arrange
    email = "test@mergington.edu"
    invalid_activity = "Invalid Activity"
    
    # Act
    response = client.post(f"/activities/{invalid_activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]


def test_unregister_success():
    # Arrange
    email = "daniel@mergington.edu"
    activity = "Chess Club"  # Activity where daniel is signed up
    
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert f"Unregistered {email} from {activity}" == result["message"]
    
    # Verify the participant was removed
    response = client.get("/activities")
    data = response.json()
    assert email not in data[activity]["participants"]


def test_unregister_not_signed_up():
    # Arrange
    email = "notsigned@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "not signed up" in result["detail"]


def test_unregister_invalid_activity():
    # Arrange
    email = "test@mergington.edu"
    invalid_activity = "Invalid Activity"
    
    # Act
    response = client.delete(f"/activities/{invalid_activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]


def test_root_redirect():
    # Arrange - No special setup needed
    
    # Act
    response = client.get("/")
    
    # Assert
    assert response.status_code == 302  # Found (default redirect status)
    assert response.headers["location"] == "/static/index.html"