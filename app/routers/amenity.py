from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.amenity import Amenity
from app.models.hall_amenity import HallAmenity
from app.models.hall import Hall
from app.schemas.amenity import AmenityCreate, AmenityResponse, HallAmenityCreate, HallAmenityResponse
from app.dependencies import get_current_user_token, role_required


router = APIRouter(prefix="/amenities", tags=["amenities"])


@router.post("/", response_model=AmenityResponse, status_code=status.HTTP_201_CREATED)
def create_amenity(
    amenity_in: AmenityCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(role_required("superadmin")),
):
    db_amenity = db.query(Amenity).filter(Amenity.amenity_name == amenity_in.amenity_name).first()
    if db_amenity:
        raise HTTPException(status_code=400, detail="Amenity already exists")
    
    db_amenity = Amenity(
        amenity_name=amenity_in.amenity_name,
        is_chargeable=amenity_in.is_chargeable,
        base_price=amenity_in.base_price,
    )
    db.add(db_amenity)
    db.commit()
    db.refresh(db_amenity)
    return db_amenity


@router.get("/", response_model=List[AmenityResponse])
def get_all_amenities(
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    amenities = db.query(Amenity).all()
    return amenities


@router.post("/hall/{hall_id}", response_model=HallAmenityResponse, status_code=status.HTTP_201_CREATED)
def add_amenity_to_hall(
    hall_id: int,
    amenity_link: HallAmenityCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    user_id = int(payload.get("sub"))
    role = payload.get("role")
    
    db_hall = db.query(Hall).filter(Hall.hall_id == hall_id).first()
    if not db_hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    
    if db_hall.subadmin_id != user_id and role != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized to modify this hall")
    
    db_amenity = db.query(Amenity).filter(Amenity.amenity_id == amenity_link.amenity_id).first()
    if not db_amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")
    
    existing = db.query(HallAmenity).filter(
        HallAmenity.hall_id == hall_id,
        HallAmenity.amenity_id == amenity_link.amenity_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Amenity already added to hall")
    
    db_hall_amenity = HallAmenity(
        hall_id=hall_id,
        amenity_id=amenity_link.amenity_id,
        custom_price=amenity_link.custom_price,
        is_active=amenity_link.is_active,
    )
    db.add(db_hall_amenity)
    db.commit()
    db.refresh(db_hall_amenity)
    return db_hall_amenity


@router.get("/hall/{hall_id}", response_model=List[HallAmenityResponse])
def get_hall_amenities(
    hall_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    db_hall = db.query(Hall).filter(Hall.hall_id == hall_id).first()
    if not db_hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    
    amenities = db.query(HallAmenity).filter(HallAmenity.hall_id == hall_id).all()
    return amenities


@router.put("/hall/{amenity_link_id}/price", response_model=HallAmenityResponse)
def update_hall_amenity_price(
    amenity_link_id: int,
    price_update: dict,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    user_id = int(payload.get("sub"))
    role = payload.get("role")
    
    db_hall_amenity = db.query(HallAmenity).filter(HallAmenity.id == amenity_link_id).first()
    if not db_hall_amenity:
        raise HTTPException(status_code=404, detail="Hall amenity not found")
    
    db_hall = db.query(Hall).filter(Hall.hall_id == db_hall_amenity.hall_id).first()
    if db_hall.subadmin_id != user_id and role != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized to modify this hall")
    
    if "custom_price" in price_update and price_update["custom_price"] is not None:
        if price_update["custom_price"] <= 0:
            raise HTTPException(status_code=400, detail="Price must be greater than 0")
        db_hall_amenity.custom_price = price_update["custom_price"]
    
    db.commit()
    db.refresh(db_hall_amenity)
    return db_hall_amenity


@router.delete("/hall/{amenity_link_id}")
def remove_amenity_from_hall(
    amenity_link_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    user_id = int(payload.get("sub"))
    role = payload.get("role")
    
    db_hall_amenity = db.query(HallAmenity).filter(HallAmenity.id == amenity_link_id).first()
    if not db_hall_amenity:
        raise HTTPException(status_code=404, detail="Hall amenity not found")
    
    db_hall = db.query(Hall).filter(Hall.hall_id == db_hall_amenity.hall_id).first()
    if db_hall.subadmin_id != user_id and role != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized to modify this hall")
    
    db_hall_amenity.is_active = False
    db.commit()
    
    return {"message": "Amenity removed from hall"}
