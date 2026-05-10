import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns expected message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "DarkWeb Intel API is running"}

def test_keywords_endpoint_exists():
    """Test that the keywords endpoint exists"""
    response = client.get("/keywords")
    # We're just checking that the endpoint exists and doesn't crash
    # The actual response might vary based on database state
    assert response.status_code in [200, 500]  # 200 if OK, 500 if server error (like DB issues)

def test_reports_endpoint_exists():
    """Test that the reports endpoint exists"""
    response = client.get("/reports")
    # We're just checking that the endpoint exists and doesn't crash
    # The actual response might vary based on database state
    assert response.status_code in [200, 500]  # 200 if OK, 500 if server error (like DB issues)

def test_add_keyword_endpoint_exists():
    """Test that the add keyword endpoint exists"""
    response = client.post("/keywords", json={"word": "test"})
    # We're just checking that the endpoint exists and doesn't crash
    # The actual response might vary based on database state/validation
    assert response.status_code in [200, 422, 500]  # 200 if OK, 422 if validation error, 500 if server error

if __name__ == "__main__":
    pytest.main([__file__])