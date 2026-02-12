from fastapi import APIRouter, Depends
from app.dependencies import role_required

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/protected")
def protected_admin(payload: dict = Depends(role_required("superadmin"))):
    return {"message": "Welcome, superadmin.", "user": {"user_id": payload.get("sub"), "role": payload.get("role")}}
