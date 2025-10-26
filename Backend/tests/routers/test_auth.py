import sys
import os
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.routers.auth import router, LoginRequest, RefreshRequest, TokenResponse
from app.db.users import UserRole
from app.services.auth import create_access_token, create_refresh_token, get_secret_key
from app.dependencies import get_mongo_db
from unittest.mock import patch, Mock, AsyncMock
import pytest
from jose import jwt
from datetime import datetime, timedelta
from pymongo.database import Database
from bson.objectid import ObjectId

app = FastAPI()
app.include_router(router)

@pytest.fixture
def client():
    """Provide a TestClient with mocked dependencies."""
    # Override the database dependency
    async def override_get_mongo_db():
        return AsyncMock()
    
    app.dependency_overrides[get_mongo_db] = override_get_mongo_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def fixed_time():
    """Provide a fixed timestamp for consistent token expiration."""
    return 1609459200  # Jan 1, 2021, 00:00:00 UTC

@pytest.fixture
def valid_user_data():
    """Provide valid user data for signup."""
    return {
        "email": "test@example.com", 
        "password": "Testpass123!", 
        "full_name": "Test User",
        "role": "user"  # Use string instead of UserRole enum
    }

@pytest.fixture
def login_request():
    """Provide valid login data."""
    return {
        "email": "test@example.com", 
        "password": "Testpass123!"
    }

@pytest.fixture
def refresh_request():
    """Generate a valid refresh token request."""
    with patch("app.services.auth.get_secret_key", return_value="test-secret-key"):
        with patch("time.time", return_value=1609459200):
            token = create_refresh_token({
                "sub": str(ObjectId("507f1f77bcf86cd799439011")), 
                "role": "user"
            })
            return {"refresh_token": token}

@pytest.fixture
def expired_refresh_token():
    """Generate an expired refresh token."""
    with patch("app.services.auth.get_secret_key", return_value="test-secret-key"):
        with patch("time.time", return_value=1609459200 - 60):  # Expired 1 minute before
            return create_refresh_token({
                "sub": str(ObjectId("507f1f77bcf86cd799439011")), 
                "role": "user"  
            })

# Tests for /api/auth/signup
def test_signup_happy_path(client, valid_user_data):
    """Test successful user signup."""
    with patch("app.routers.auth.create_user") as mock_create_user:
        mock_create_user.return_value = "507f1f77bcf86cd799439011"
        
        response = client.post("/api/auth/signup", json=valid_user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "User created"
        assert data["user_id"] == "507f1f77bcf86cd799439011"

def test_signup_failure(client, valid_user_data):
    """Test signup failure when create_user returns None."""
    with patch("app.routers.auth.create_user") as mock_create_user:
        mock_create_user.return_value = None
        
        response = client.post("/api/auth/signup", json=valid_user_data)
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "User creation failed"

def test_signup_invalid_data(client):
    """Test signup with invalid data (missing email)."""
    invalid_data = {
        "password": "Testpass123!", 
        "full_name": "Test User",
        "role": "user"
    }
    response = client.post("/api/auth/signup", json=invalid_data)
    assert response.status_code == 422  # Unprocessable Entity due to Pydantic validation

# Tests for /api/auth/login
def test_login_happy_path(client, login_request):
    """Test successful login with valid credentials."""
    with patch("app.routers.auth.authenticate_user") as mock_authenticate:
        mock_authenticate.return_value = {
            "_id": ObjectId("507f1f77bcf86cd799439011"), 
            "role": "user"  
        }
        with patch("app.routers.auth.create_access_token") as mock_access_token:
            with patch("app.routers.auth.create_refresh_token") as mock_refresh_token:
                mock_access_token.return_value = "mock.access.token"
                mock_refresh_token.return_value = "mock.refresh.token"
                
                response = client.post("/api/auth/login", json=login_request)
                assert response.status_code == 200
                data = response.json()
                assert isinstance(data, dict)
                assert "access_token" in data
                assert "refresh_token" in data
                assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client, login_request):
    """Test login with invalid credentials."""
    with patch("app.routers.auth.authenticate_user") as mock_authenticate:
        mock_authenticate.return_value = None
        
        response = client.post("/api/auth/login", json=login_request)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid credentials"

def test_login_missing_user(client, login_request):
    """Test login with non-existent user."""
    with patch("app.routers.auth.authenticate_user") as mock_authenticate:
        mock_authenticate.return_value = None
        
        response = client.post("/api/auth/login", json=login_request)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid credentials"

# Tests for /api/auth/refresh
def test_refresh_happy_path(client):
    """Test successful token refresh with valid refresh token."""
    refresh_payload = {
        "sub": "507f1f77bcf86cd799439011",
        "role": "user",
        "type": "refresh"
    }
    
    with patch("app.routers.auth.get_secret_key") as mock_secret_key:
        with patch("app.routers.auth._get_collection") as mock_get_collection:
            with patch("app.routers.auth.create_access_token") as mock_access_token:
                with patch("app.routers.auth.create_refresh_token") as mock_refresh_token:
                    mock_secret_key.return_value = "test-secret-key"
                    
                    mock_collection = AsyncMock()
                    mock_collection.find_one.return_value = {
                        "_id": ObjectId("507f1f77bcf86cd799439011"), 
                        "role": "user"
                    }
                    mock_get_collection.return_value = mock_collection
                    
                    mock_access_token.return_value = "new.access.token"
                    mock_refresh_token.return_value = "new.refresh.token"
                    
                    valid_refresh_token = jwt.encode(refresh_payload, "test-secret-key", algorithm="HS256")
                    refresh_data = {"refresh_token": valid_refresh_token}
                    
                    response = client.post("/api/auth/refresh", json=refresh_data)
                    assert response.status_code == 200
                    data = response.json()
                    assert isinstance(data, dict)
                    assert "access_token" in data
                    assert "refresh_token" in data
                    assert data["token_type"] == "bearer"

def test_refresh_expired_token(client):
    """Test refresh with an expired token."""
    # Mock the JWT decode to raise ExpiredSignatureError
    with patch("app.routers.auth.get_secret_key") as mock_secret_key:
        with patch("app.routers.auth.jwt.decode") as mock_jwt_decode:
            mock_secret_key.return_value = "test-secret-key"
            mock_jwt_decode.side_effect = jwt.ExpiredSignatureError("Token expired")
            
            refresh_data = {"refresh_token": "expired-token"}
            response = client.post("/api/auth/refresh", json=refresh_data)
            assert response.status_code == 401
            data = response.json()
            assert data["detail"] == "Refresh token expired"

def test_refresh_invalid_token(client):
    """Test refresh with an invalid token."""
    # Mock the JWT decode to raise JWTError
    with patch("app.routers.auth.get_secret_key") as mock_secret_key:
        with patch("app.routers.auth.jwt.decode") as mock_jwt_decode:
            mock_secret_key.return_value = "test-secret-key"
            mock_jwt_decode.side_effect = jwt.JWTError("Invalid token")
            
            refresh_data = {"refresh_token": "invalid-token"}
            response = client.post("/api/auth/refresh", json=refresh_data)
            assert response.status_code == 401
            data = response.json()
            assert data["detail"] == "Invalid refresh token"

def test_refresh_missing_user(client):
    """Test refresh with a valid token but non-existent user."""
    refresh_payload = {
        "sub": "507f1f77bcf86cd799439011",
        "role": "user",
        "type": "refresh"
    }
    
    with patch("app.routers.auth.get_secret_key") as mock_secret_key:
        with patch("app.routers.auth._get_collection") as mock_get_collection:
            mock_secret_key.return_value = "test-secret-key"
            
            mock_collection = AsyncMock()
            mock_collection.find_one.return_value = None
            mock_get_collection.return_value = mock_collection
            
            valid_token = jwt.encode(refresh_payload, "test-secret-key", algorithm="HS256")
            refresh_data = {"refresh_token": valid_token}
            
            response = client.post("/api/auth/refresh", json=refresh_data)
            assert response.status_code == 404
            data = response.json()
            assert data["detail"] == "User not found"