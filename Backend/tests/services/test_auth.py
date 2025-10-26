import sys
import os
from fastapi import HTTPException


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.services.auth import get_secret_key, authenticate_user, create_access_token, create_refresh_token
from app.db.db import _get_collection
from unittest.mock import patch, Mock, AsyncMock
import pytest
from jose import jwt
from passlib.context import CryptContext
from pymongo.database import Database
from bson.objectid import ObjectId
import time


@pytest.fixture
def pwd_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def mock_db():
    """Provide a mock MongoDB database."""
    db = Mock(spec=Database)
    collection = AsyncMock()  
    collection.find_one = AsyncMock()
    db.users = collection  
    return db

@pytest.fixture
def current_time():
    """Provide a current timestamp for token creation."""
    return int(time.time())  # Use current time as integer to avoid floating point issues

# Tests for get_secret_key
def test_get_secret_key_happy_path(monkeypatch):
    """Test retrieving a valid secret key from environment."""
    monkeypatch.setenv("JWT_SECRET", "test-secret-key")
    assert get_secret_key() == "test-secret-key"

def test_get_secret_key_missing(monkeypatch):
    """Test raising RuntimeError when JWT_SECRET is not set."""
    monkeypatch.delenv("JWT_SECRET", raising=False)
    with pytest.raises(RuntimeError, match="JWT_SECRET environment variable is not set"):
        get_secret_key()

# Tests for authenticate_user
@pytest.mark.asyncio
async def test_authenticate_user_happy_path(mock_db, pwd_context):
    """Test successful user authentication."""
    user_data = {"_id": ObjectId("507f1f77bcf86cd799439011"), "email": "test@example.com", "hashed_password": pwd_context.hash("Testpass123!")}
    
    # Mock _get_collection to return our mock collection
    with patch("app.services.auth._get_collection") as mock_get_collection:
        mock_get_collection.return_value = mock_db.users
        mock_db.users.find_one.return_value = user_data
        
        result = await authenticate_user("test@example.com", "Testpass123!", mock_db)
        assert result == user_data

@pytest.mark.asyncio
async def test_authenticate_user_invalid_password(mock_db, pwd_context):
    """Test authentication failure with invalid password."""
    user_data = {"_id": ObjectId("507f1f77bcf86cd799439011"), "email": "test@example.com", "hashed_password": pwd_context.hash("Testpass123!")}
    
    with patch("app.services.auth._get_collection") as mock_get_collection:
        mock_get_collection.return_value = mock_db.users
        mock_db.users.find_one.return_value = user_data
        
        result = await authenticate_user("test@example.com", "Wrongpass123!", mock_db)
        assert result is None

@pytest.mark.asyncio
async def test_authenticate_user_missing_user(mock_db):
    """Test authentication with non-existent user."""
    with patch("app.services.auth._get_collection") as mock_get_collection:
        mock_get_collection.return_value = mock_db.users
        mock_db.users.find_one.return_value = None
        
        result = await authenticate_user("nonexistent@example.com", "Testpass123!", mock_db)
        assert result is None

# Tests for create_access_token
def test_create_access_token_happy_path(current_time):
    """Test creating a valid access token."""
    with patch("app.services.auth.get_secret_key", return_value="test-secret-key"):
        with patch("time.time", return_value=current_time):
            data = {"sub": "user123", "role": "user"}
            token = create_access_token(data)
            assert isinstance(token, str)
            payload = jwt.decode(token, "test-secret-key", algorithms=["HS256"])
            assert payload["sub"] == "user123"
            assert payload["role"] == "user"
            assert payload["exp"] == current_time + (15 * 60) 

def test_create_access_token_edge_case_large_data(current_time):
    """Test creating a token with large data."""
    with patch("app.services.auth.get_secret_key", return_value="test-secret-key"):
        with patch("time.time", return_value=current_time):
            large_data = {"sub": "user123", "role": "user", "extra": "x" * 1000}
            token = create_access_token(large_data)
            assert isinstance(token, str)
            payload = jwt.decode(token, "test-secret-key", algorithms=["HS256"])
            assert payload["sub"] == "user123"
            assert payload["role"] == "user"
            assert payload["extra"] == "x" * 1000
            assert payload["exp"] == current_time + (15 * 60)

# Tests for create_refresh_token
def test_create_refresh_token_happy_path(current_time):
    """Test creating a valid refresh token."""
    with patch("app.services.auth.get_secret_key", return_value="test-secret-key"):
        with patch("time.time", return_value=current_time):
            data = {"sub": "user123", "role": "user"}
            token = create_refresh_token(data)
            assert isinstance(token, str)
            payload = jwt.decode(token, "test-secret-key", algorithms=["HS256"])
            assert payload["sub"] == "user123"
            assert payload["role"] == "user"
            assert payload["type"] == "refresh"
            assert payload["exp"] == current_time + (7 * 24 * 60 * 60)
def test_create_refresh_token_edge_case_expired(current_time):
    """Test creating a token that would be expired with manipulated time."""
    with patch("app.services.auth.get_secret_key", return_value="test-secret-key"):
        # Use a time far in the future to test token creation
        future_time = current_time + (7 * 24 * 60 * 60) + 1  # 1 second past 7 days from current_time
        with patch("time.time", return_value=future_time):
            data = {"sub": "user123", "role": "user"}
            token = create_refresh_token(data)
            # The token should be created with expiration in the future relative to future_time
            payload = jwt.decode(token, "test-secret-key", algorithms=["HS256"])
            expected_exp = future_time + (7 * 24 * 60 * 60)  # 7 days from future_time
            assert payload["exp"] == expected_exp