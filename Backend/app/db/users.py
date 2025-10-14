# app/db/users.py
from typing import Optional
from pydantic import BaseModel, EmailStr
from bson import ObjectId
from pymongo.database import Database
from pymongo.collection import Collection
from passlib.context import CryptContext
from loguru import logger
from .db import _get_collection

class UserBase(BaseModel):
    email: EmailStr
    role: str  # e.g., "admin" or "user"

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: Optional[ObjectId] = None
    hashed_password: str
    
    # Allow arbitrary types like ObjectId
    model_config = {
        "arbitrary_types_allowed": True
    }

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(user_data: UserCreate, mongo_db: Database = None) -> Optional[ObjectId]:
    """Create a new user with hashed password."""
    if mongo_db is None:
        raise RuntimeError("Database connection not initialized")
    collection = _get_collection(mongo_db, "users")
    user_dict = user_data.dict()
    # Clean and encode password, truncate to 72 bytes
    password = user_data.password.strip()  # Remove any trailing whitespace/newlines
    password_bytes = password.encode('utf-8')[:72]
    logger.debug(f"Hashing password: {password} (length: {len(password_bytes)} bytes)")
    # Hash as bytes
    user_dict["hashed_password"] = pwd_context.hash(password_bytes)
    del user_dict["password"]
    try:
        result = await collection.insert_one(user_dict)
        return result.inserted_id
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        return None

async def seed_admin(mongo_db: Database = None) -> None:
    """Seed a default admin user if none exists."""
    if mongo_db is None:
        raise RuntimeError("Database connection not initialized")
    collection = _get_collection(mongo_db, "users")
    admin = await collection.find_one({"role": "admin"})
    if not admin:
        admin_data = UserCreate(email="admin@example.com", role="admin", password="admin123")
        inserted_id = await create_user(admin_data, mongo_db)
        if inserted_id:
            logger.info("Admin user seeded successfully.")
        else:
            logger.error("Failed to seed admin user.")