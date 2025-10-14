from fastapi import APIRouter, HTTPException, status, Depends
from app.db.users import create_user, UserCreate
from app.services.auth import authenticate_user, create_access_token
from app.dependencies import get_mongo_db  # Assume this exists or create it
from pymongo.database import Database
from pydantic import BaseModel  # Add this import

# New model for login request
class LoginRequest(BaseModel):
    email: str
    password: str

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/signup", response_model=dict, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, mongo_db: Database = Depends(get_mongo_db)):
    user_id = await create_user(user, mongo_db)
    if not user_id:
        raise HTTPException(status_code=400, detail="User creation failed")
    return {"message": "User created", "user_id": str(user_id)}

@router.post("/login", response_model=dict)
async def login(login_data: LoginRequest, mongo_db: Database = Depends(get_mongo_db)):
    user = await authenticate_user(login_data.email, login_data.password, mongo_db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user["_id"]), "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}