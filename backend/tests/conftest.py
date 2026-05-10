import pytest
import asyncio
from tortoise import Tortoise

@pytest.fixture(scope="session", autouse=True)
def initialize_tests():
    """Initialize test database"""
    # Create a new event loop for the session
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Initialize Tortoise with in-memory SQLite database
    loop.run_until_complete(Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.models.models"]}
    ))
    # Generate schemas
    loop.run_until_complete(Tortoise.generate_schemas())
    yield
    # Close connections
    loop.run_until_complete(Tortoise.close_connections())
    loop.close()