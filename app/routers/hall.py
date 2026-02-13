from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.database import get_db
from app.models.hall import Hall
from app.schemas.hall import HallCreate, HallUpdate, HallResponse
from app.dependencies import get_current_user_token, role_required


class HallStatusUpdate(BaseModel):
    status: str


router = APIRouter(prefix="/halls", tags=["halls"])


@router.post("/", response_model=HallResponse, status_code=status.HTTP_201_CREATED)
def create_hall(
    hall_in: HallCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    user_id = payload.get("sub")
    
    db_hall = Hall(
        hall_name=hall_in.hall_name,
        location=hall_in.location,
        capacity=hall_in.capacity,
        base_price=hall_in.base_price,
        commission_percent=hall_in.commission_percent,
        description=hall_in.description,
        subadmin_id=user_id,
        status="pending",
    )
    db.add(db_hall)
    db.commit()
    db.refresh(db_hall)
    return db_hall


@router.get("/my-halls", response_model=List[HallResponse])
def get_my_halls(
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    user_id = payload.get("sub")
    halls = db.query(Hall).filter(Hall.subadmin_id == user_id).all()
    return halls


@router.get("/", response_model=List[HallResponse])
def get_all_halls(
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    # Superadmin gets all halls, others get only approved halls
    role = payload.get("role")
    if role == "superadmin":
        halls = db.query(Hall).all()
    else:
        halls = db.query(Hall).filter(Hall.status == "approved").all()
    return halls


@router.put("/{hall_id}", response_model=HallResponse)
def update_hall(
    hall_id: int,
    hall_in: HallUpdate,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    user_id = payload.get("sub")
    
    db_hall = db.query(Hall).filter(Hall.hall_id == hall_id).first()
    if not db_hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    
    if db_hall.subadmin_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this hall")
    
    if db_hall.status == "approved":
        raise HTTPException(status_code=400, detail="Cannot update approved hall")
    
    update_data = hall_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_hall, field, value)
    
    db.commit()
    db.refresh(db_hall)
    return db_hall


@router.delete("/{hall_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hall(
    hall_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    user_id = payload.get("sub")
    
    db_hall = db.query(Hall).filter(Hall.hall_id == hall_id).first()
    if not db_hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    
    if db_hall.subadmin_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this hall")
    
    db_hall.status = "blocked"
    db.commit()


@router.patch("/{hall_id}/status", response_model=HallResponse)
def update_hall_status(
    hall_id: int,
    status_update: HallStatusUpdate,
    db: Session = Depends(get_db),
    payload: dict = Depends(role_required("superadmin")),
):
    db_hall = db.query(Hall).filter(Hall.hall_id == hall_id).first()
    if not db_hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    
    if status_update.status not in ["approved", "blocked"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'approved' or 'blocked'")
    
    db_hall.status = status_update.status
    db.commit()
    db.refresh(db_hall)
    return db_hall
