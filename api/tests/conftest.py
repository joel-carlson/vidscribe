import pytest
from unittest.mock import patch
from starlette.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(autouse=True)
def mock_pubsub():
    """Mock Pub/Sub for every test so no real messages are sent."""
    with patch("db.publish_job") as mock:
        mock.return_value = None
        yield mock


@pytest.fixture
async def db():
    """Create a Database instance within the test's event loop for DB tests."""
    from db import Database
    instance = await Database.create()
    yield instance
    await instance.disconnect()


@pytest.fixture
def client():
    """FastAPI TestClient using the app's own lifespan for API tests."""
    from main import app
    with TestClient(app) as c:
        yield c
