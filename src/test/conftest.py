from src.db.main import get_session
from src import app
from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient
from src.auth.dependencies import RoleChecker, AccessTokenBearer, RefreshTokenBearer

mock_session = Mock()
mock_user_service = Mock()
mock_book_service = Mock()

def get_mock_session():
  yield mock_session

access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()
role_checker = RoleChecker(['admin'])

app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[role_checker] = Mock()
app.dependency_overrides[AccessTokenBearer] = Mock()
app.dependency_overrides[RefreshTokenBearer] = Mock()

@pytest.fixture(scope="session")
def fake_session():
    """Fixture to provide a mock session for testing."""
    return mock_session
@pytest.fixture(scope="session")
def mock_user_service():
    """Fixture to provide a mock user service for testing."""
    return mock_user_service
@pytest.fixture(scope="session")
def fake_book_service():
    """Fixture to provide a mock user service for testing."""
    return mock_book_service
@pytest.fixture(scope="module")
def test_client():
    """Fixture to provide a test client for the FastAPI app."""
    with TestClient(app) as client:
        yield client