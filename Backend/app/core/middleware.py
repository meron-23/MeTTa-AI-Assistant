from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
import os

SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key")
ALGORITHM = "HS256"

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/auth/"):  # Allow auth endpoints without token
            return await call_next(request)
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="No token provided")
        try:
            payload = jwt.decode(token[7:], SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = {"id": payload["sub"], "role": payload["role"]}
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        response = await call_next(request)
        return response