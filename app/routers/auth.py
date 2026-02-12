from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.services import security as sec
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Basic register - does not perform strong validation intentionally
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = sec.get_password_hash(user_in.password)
    db_user = User(full_name=user_in.full_name, email=user_in.email, password=hashed, role=user_in.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm provides username and password fields; we use username as email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not sec.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=60)
    token = sec.create_access_token(subject=user.user_id, role=user.role, expires_delta=access_token_expires)

    return {"access_token": token, "token_type": "bearer", "role": user.role}
