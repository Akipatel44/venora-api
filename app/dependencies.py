from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.security import decode_access_token

bearer_scheme = HTTPBearer()


def get_current_user_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload


def role_required(*allowed_roles):
    def _dependency(payload: dict = Depends(get_current_user_token)):
        role = payload.get("role")
        if role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient role")
        return payload

    return _dependency
