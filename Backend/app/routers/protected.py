from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

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

@router.get("/admin-only")
async def admin_only(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"message": "Admin only route"}