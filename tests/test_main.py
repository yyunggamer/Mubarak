import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    """Test the root endpoint /"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Hello from Flask running in an Alpine-based Docker container!"


def test_health(client):
    """Test the /health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "OK"
    assert data["container"] == "alpine_python"
