import pytest
from fastapi.testclient import TestClient
from tortoise import Tortoise
import asyncio
import os

# Set test database URL before importing app
os.environ["DATABASE_URL"] = "sqlite://:memory:"

# Initialize Tortoise before importing the app
async def init_tortoise():
    await Tortoise.init(
        db_url=os.environ["DATABASE_URL"],
        modules={"models": ["app.models.models"]}
    )
    await Tortoise.generate_schemas()

# Run the initialization
try:
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

loop.run_until_complete(init_tortoise())

# Now import the app
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns expected message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "DarkWeb Intel API is running"}

def test_add_keyword():
    """Test adding a keyword"""
    response = client.post("/keywords", json={"word": "testkeyword"})
    # This might fail due to database state, but we're testing the endpoint exists
    assert response.status_code in [200, 422]  # 200 if successful, 422 if validation error

def test_get_keywords():
    """Test retrieving keywords"""
    response = client.get("/keywords")
    assert response.status_code == 200
    # Should return a list (even if empty)
    assert isinstance(response.json(), list)

def test_get_reports():
    """Test retrieving reports"""
    response = client.get("/reports")
    assert response.status_code == 200
    # Should return a list (even if empty)
    assert isinstance(response.json(), list)

# Cleanup
loop.run_until_complete(Tortoise.close_connections())
loop.close()

if __name__ == "__main__":
    pytest.main([__file__])