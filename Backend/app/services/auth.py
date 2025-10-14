from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional, Dict
from pymongo.database import Database
from loguru import logger
import os
from app.db.db import _get_collection  # Reuse existing collection getter
import time

SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def authenticate_user(email: str, password: str, mongo_db: Database) -> Optional[Dict]:
    collection = _get_collection(mongo_db, "users")
    user = await collection.find_one({"email": email})
    if user and pwd_context.verify(password, user["hashed_password"]):
        return user
    return None

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
    to_encode.update({"exp": int(time.time()) + expire})  # Current time + expire time
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt