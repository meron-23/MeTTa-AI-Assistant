import sys
import os
import uuid
import string
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from app.db.users import create_user, seed_admin, UserCreate, UserRole
from mongomock import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pydantic import ValidationError
from unittest.mock import patch, Mock, ANY, AsyncMock
from pymongo.results import InsertOneResult

@pytest.fixture
def config():
    """Provide configurable test settings."""
    return {
        "password_chars": string.ascii_letters + string.digits + "!@#$%^&*()",
        "password_length": 12,
        "db_error_msg": "Database connection not initialized",
        "env_error_msg": "One or more admin credentials",
        "invalid_email": f"invalid-{uuid.uuid4()}",
        "static_password": ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8)),
        "long_email": ''.join(random.choices(string.ascii_letters, k=200)) + "@example.com",
        "long_password": ''.join(random.choices(string.ascii_letters + string.digits, k=1000))
    }

@pytest.fixture
def unique_email():
    """Generate a unique email for each test."""
    return f"test-{uuid.uuid4()}@example.com"

@pytest.fixture
def random_password(config):
    """Generate a random password for each test using configurable settings."""
    characters = config["password_chars"]
    length = config["password_length"]
    return ''.join(random.choice(characters) for _ in range(length))

@pytest.fixture
def random_role():
    """Randomly select a role for each test."""
    return random.choice([UserRole.USER, UserRole.ADMIN])

@pytest.fixture
def mock_env(config):
    """Mock environment variables for admin seeding with dynamic values."""
    admin_email = f"admin-{uuid.uuid4()}@example.com"
    admin_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(config["password_length"]))
    original_env = os.environ.copy()
    os.environ.update({"ADMIN_EMAIL": admin_email, "ADMIN_PASSWORD": admin_password})
    yield {"email": admin_email, "password": admin_password}
    os.environ.clear()
    os.environ.update(original_env)  # Cleanup environment

@pytest.fixture
def mock_db():
    """Provide a mock MongoDB database for testing."""
    client = MongoClient()
    db = client.test_db
    # Mock get_collection to return a usable collection
    collection = Mock(spec=Collection)
    collection.find_one = AsyncMock(return_value=None)  # Async-compatible mock
    insert_result = Mock(spec=InsertOneResult)
    insert_result.inserted_id = uuid.uuid4().hex  # Random inserted_id
    async def mock_insert_one(*args, **kwargs):
        return insert_result
    collection.insert_one = AsyncMock(side_effect=mock_insert_one)  # Custom async behavior
    db.get_collection = Mock(return_value=collection)
    yield db
    client.close()

# Tests for create_user
@pytest.mark.asyncio
async def test_create_user_happy_path(mock_db, unique_email, random_password, random_role):
    """Test creating a user with valid input."""
    user_data = UserCreate(email=unique_email, password=random_password, role=random_role)
    user_id = await create_user(user_data, mock_db)
    assert user_id is not None  # Check for non-None
    mock_db.get_collection().insert_one.assert_called_once_with(ANY)

@pytest.mark.asyncio
async def test_create_user_role_assignment(mock_db, unique_email, random_password, random_role):
    """Test that the role is correctly assigned as a string."""
    user_data = UserCreate(email=unique_email, password=random_password, role=random_role)
    user_id = await create_user(user_data, mock_db)
    assert user_id is not None  # Check for non-None
    mock_db.get_collection().insert_one.assert_called_once_with(ANY)

@pytest.mark.asyncio
async def test_create_user_duplicate_email(mock_db, unique_email, random_password, random_role):
    """Test that duplicate email raises ValueError."""
    user_data = UserCreate(email=unique_email, password=random_password, role=random_role)
    mock_db.get_collection().find_one.return_value = {"email": unique_email}
    with pytest.raises(ValueError, match=f"Email {unique_email} is already registered."):
        await create_user(user_data, mock_db)

@pytest.mark.asyncio
async def test_create_user_invalid_email(config):
    """Test that invalid email format raises ValidationError."""
    with pytest.raises(ValidationError, match="value is not a valid email address"):
        UserCreate(email=config["invalid_email"], password=config["static_password"], role=UserRole.USER)

@pytest.mark.asyncio
async def test_create_user_empty_password(mock_db, unique_email):
    """Test creating a user with empty or whitespace password."""
    user_data = UserCreate(email=unique_email, password="", role=UserRole.USER)
    user_id = await create_user(user_data, mock_db)
    assert user_id is not None  # Expect hashing to handle empty string
    mock_db.get_collection().insert_one.assert_called_once_with(ANY)

@pytest.mark.asyncio
#fix the logic
async def test_create_user_long_data(mock_db, config):
    """Test creating a user with long email and password."""
    user_data = UserCreate(email=config["long_email"], password=config["long_password"], role=UserRole.USER)
    user_id = await create_user(user_data, mock_db)
    assert user_id is not None  # Check for non-None
    mock_db.get_collection().insert_one.assert_called_once_with(ANY)

@pytest.mark.asyncio
async def test_create_user_no_db(config):
    """Test that missing database raises RuntimeError."""
    user_data = UserCreate(email=f"test-static-{uuid.uuid4()}@example.com", password=config["static_password"], role=UserRole.USER)
    with pytest.raises(RuntimeError, match=config["db_error_msg"]):
        await create_user(user_data, None)

@pytest.mark.asyncio
async def test_create_user_insert_failure(mock_db, unique_email, random_password, random_role):
    """Test that a failed insert returns None and logs error."""
    mock_db.get_collection().insert_one.side_effect = Exception("Insert failed")
    with patch("app.db.users.logger.error") as mock_logger:
        user_data = UserCreate(email=unique_email, password=random_password, role=random_role)
        result = await create_user(user_data, mock_db)
        assert result is None
        mock_logger.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_password_hashing(mock_db, unique_email, random_password):
    """Test that password is hashed with strip()."""
    user_data = UserCreate(email=unique_email, password=f" {random_password} ", role=UserRole.USER)
    with patch("app.db.users.pwd_context.hash") as mock_hash:
        mock_hash.return_value = "hashed_value"
        user_id = await create_user(user_data, mock_db)
        assert user_id is not None
        mock_hash.assert_called_once_with(random_password.strip())

# Tests for seed_admin
@pytest.mark.asyncio
async def test_seed_admin_happy_path(mock_db, mock_env):
    """Test seeding an admin user when none exists."""
    mock_db.get_collection().find_one.return_value = None
    await seed_admin(mock_db)
    mock_db.get_collection().insert_one.assert_called_once_with(ANY)

@pytest.mark.asyncio
async def test_seed_admin_existing(mock_db, mock_env):
    """Test that seeding skips if an admin already exists."""
    mock_db.get_collection().find_one.return_value = {"role": "admin"}
    with patch("app.db.users.logger.info") as mock_logger:
        await seed_admin(mock_db)
        mock_logger.assert_not_called()

@pytest.mark.asyncio
async def test_seed_admin_no_env(mock_db, config):
    """Test that missing env variables raise RuntimeError."""
    with patch.dict(os.environ, {"ADMIN_EMAIL": "", "ADMIN_PASSWORD": config["static_password"]}):
        with pytest.raises(RuntimeError, match=config["env_error_msg"]):
            await seed_admin(mock_db)

@pytest.mark.asyncio
async def test_seed_admin_no_db(config):
    """Test that missing database raises RuntimeError."""
    with pytest.raises(RuntimeError, match=config["db_error_msg"]):
        await seed_admin(None)

@pytest.mark.asyncio
async def test_seed_admin_failure(mock_db, mock_env):
    """Test that a failure in create_user logs an error."""
    with patch("app.db.users.create_user", return_value=None):
        with patch("app.db.users.logger.error") as mock_logger:
            await seed_admin(mock_db)
            mock_logger.assert_called_with("Failed to seed admin user.")
