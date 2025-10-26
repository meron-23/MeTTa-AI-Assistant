import sys
import os
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException
import pytest
from jose import jwt
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.db.users import UserRole
from app.services.auth import create_access_token

app = FastAPI()

from app.routers.protected import router
app.include_router(router)

@pytest.fixture
def admin_user():
    return {"_id": "507f1f77bcf86cd799439011", "role": UserRole.ADMIN.value}

@pytest.fixture
def user_user():
    return {"_id": "507f1f77bcf86cd799439012", "role": UserRole.USER.value}

@pytest.fixture
def admin_token(admin_user):
    """Generate a valid test access token for an admin user."""
    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.services.auth.get_secret_key", lambda: "test-secret-key")
        m.setattr("time.time", lambda: 1609459200)
        return create_access_token({"sub": admin_user["_id"], "role": admin_user["role"]})

@pytest.fixture
def user_token(user_user):
    """Generate a valid test access token for a regular user."""
    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.services.auth.get_secret_key", lambda: "test-secret-key")
        m.setattr("time.time", lambda: 1609459200)
        return create_access_token({"sub": user_user["_id"], "role": user_user["role"]})

@pytest.fixture
def expired_token(admin_user):
    """Generate an expired test access token."""
    expired_payload = {
        "sub": admin_user["_id"], 
        "role": admin_user["role"],
        "exp": datetime.utcnow().timestamp() - 3600
    }
    return jwt.encode(expired_payload, "test-secret-key", algorithm="HS256")

# Mock functions for different scenarios
def mock_admin_user():
    return {"_id": "507f1f77bcf86cd799439011", "role": UserRole.ADMIN.value}

def mock_regular_user():
    return {"_id": "507f1f77bcf86cd799439012", "role": UserRole.USER.value}

def mock_no_user():
    raise HTTPException(status_code=401, detail="Not authenticated")

def mock_user_missing_role():
    return {"_id": "507f1f77bcf86cd799439011"}  

@pytest.fixture
def client():
    """Generic test client."""
    return TestClient(app)

# All 6 tests from your original code
def test_admin_only_happy_path(client):
    """Test successful access to admin-only route with valid admin token."""
    from app.routers.protected import get_current_user
    app.dependency_overrides[get_current_user] = mock_admin_user
    
    response = client.get("/api/protected/admin-only")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Admin only route"
    
    app.dependency_overrides.clear()

def test_admin_only_unauthenticated(client):
    """Test access to admin-only route without authentication."""
    from app.routers.protected import get_current_user
    app.dependency_overrides[get_current_user] = mock_no_user
    
    response = client.get("/api/protected/admin-only")
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Not authenticated"
    
    app.dependency_overrides.clear()

def test_admin_only_wrong_role(client):
    """Test access to admin-only route with valid non-admin token."""
    from app.routers.protected import get_current_user
    app.dependency_overrides[get_current_user] = mock_regular_user
    
    response = client.get("/api/protected/admin-only")
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "admin access required"
    
    app.dependency_overrides.clear()

def test_admin_only_invalid_token(client):
    """Test access to admin-only route with an invalid token."""
    # For this test, we don't override the dependency - let it use the real one
    # which will fail with invalid token
    response = client.get("/api/protected/admin-only", headers={"Authorization": "Bearer invalid-token"})
    assert response.status_code == 401
    data = response.json()
    assert "Invalid token" in data["detail"] or "Not authenticated" in data["detail"]

def test_admin_only_expired_token(client):
    """Test access to admin-only route with an expired token."""
    # Mock the get_secret_key function to avoid environment variable issues
    with pytest.MonkeyPatch().context() as m:
        m.setattr("app.services.auth.get_secret_key", lambda: "test-secret-key-for-jwt")
        
        # Create an expired token using the mocked secret key
        expired_token = jwt.encode(
            {"sub": "user123", "role": "user", "exp": datetime.utcnow().timestamp() - 3600},
            "test-secret-key-for-jwt",
            algorithm="HS256"
        )
        
        response = client.get("/api/protected/admin-only", headers={"Authorization": f"Bearer {expired_token}"})
        assert response.status_code == 401

def test_admin_only_missing_user(client):
    """Test access to admin-only route with a token but missing user data."""
    def mock_user_invalid_role():
        return {"_id": "507f1f77bcf86cd799439011", "role": "invalid_role"}
    
    from app.routers.protected import get_current_user
    app.dependency_overrides[get_current_user] = mock_user_invalid_role
    
    response = client.get("/api/protected/admin-only")
    assert response.status_code == 403
    data = response.json()
    assert "admin access required" in data["detail"]
    
    app.dependency_overrides.clear()

def test_admin_only_malformed_token(client):
    """Test access with malformed JWT token."""
    response = client.get("/api/protected/admin-only", headers={"Authorization": "Bearer malformed.jwt.token"})
    assert response.status_code == 401

def test_admin_only_wrong_secret_token(client):
    """Test access with token signed with wrong secret."""
    wrong_secret_token = jwt.encode(
        {"sub": "user123", "role": "admin"}, 
        "wrong-secret-key", 
        algorithm="HS256"
    )
    response = client.get("/api/protected/admin-only", headers={"Authorization": f"Bearer {wrong_secret_token}"})
    assert response.status_code == 401

def test_admin_only_case_sensitive_roles(client):
    """Test role comparison is case-sensitive."""
    def mock_upper_case_admin():
        return {"_id": "admin123", "role": "ADMIN"}  
    
    from app.routers.protected import get_current_user
    app.dependency_overrides[get_current_user] = mock_upper_case_admin
    
    response = client.get("/api/protected/admin-only")
    assert response.status_code == 403  # Should fail due to case mismatch
    app.dependency_overrides.clear()

def test_admin_only_token_tampering(client):
    """Test that tampered tokens are rejected."""
    # Create valid token then tamper with it
    valid_token = jwt.encode(
        {"sub": "admin123", "role": "admin"},
        "test-secret-key",
        algorithm="HS256"
    )
    tampered_token = valid_token[:-5] + "tampered"
    
    response = client.get("/api/protected/admin-only", headers={"Authorization": f"Bearer {tampered_token}"})
    assert response.status_code == 401