from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from app.db.users import UserRole 

router = APIRouter(
    prefix="/api/protected",
    tags=["protected"],
    responses={403: {"description": "Forbidden"}},
)

def get_current_user(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

def require_role(required_role: UserRole):
    def decorator(func):
        async def wrapper(*args, current_user: dict = Depends(get_current_user), **kwargs):
            if current_user["role"] != required_role:
                raise HTTPException(status_code=403, detail=f"{required_role.value} access required")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

@router.get("/admin-only")
@require_role(required_role=UserRole.ADMIN)
async def admin_only(current_user: dict):
    return {"message": "Admin only route"}