import pytest
from fastapi.testclient import TestClient
from src.app import app
import copy


@pytest.fixture
def client():
    """
    Provides a TestClient for making HTTP requests to the FastAPI app.
    Resets the activities data before each test to ensure isolation.
    """
    # Import the activities dict
    from src import app as app_module
    
    # Store the original activities
    original_activities = copy.deepcopy(app_module.activities)
    
    # Create a fresh copy for this test
    app_module.activities = copy.deepcopy(original_activities)
    
    # Create and yield the client
    test_client = TestClient(app)
    yield test_client
    
    # Restore original activities after test
    app_module.activities = original_activities


@pytest.fixture
def fresh_activities():
    """
    Provides a fresh copy of activities data for test setup.
    """
    from src import app as app_module
    return copy.deepcopy(app_module.activities)
