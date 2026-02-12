"""
Project Omni-Genesis: Root conftest.py
Provides shared test fixtures for the entire project.
"""
import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.main import app
from backend.auth import create_access_token


@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    return TestClient(app)


@pytest.fixture
def auth_token():
    """Generate a valid JWT token for testing."""
    return create_access_token(user_id="test_user")


@pytest.fixture
def auth_headers(auth_token):
    """Authorization headers with a valid Bearer token."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def admin_token():
    """Generate a valid JWT token for the admin user."""
    return create_access_token(user_id="admin")


@pytest.fixture
def admin_headers(admin_token):
    """Authorization headers for admin user."""
    return {"Authorization": f"Bearer {admin_token}"}
