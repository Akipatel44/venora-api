from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
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
    
    # Use raw SQL to insert to accommodate the existing hall_amenities schema
    check_sql = "SELECT hall_id, amenity_id FROM hall_amenities WHERE hall_id = :hall_id AND amenity_id = :amenity_id"
    found = db.execute(text(check_sql), {"hall_id": hall_id, "amenity_id": amenity_link.amenity_id}).first()
    if found:
        raise HTTPException(status_code=400, detail="Amenity already added to hall")

    insert_sql = """
    INSERT INTO hall_amenities (hall_id, amenity_id, custom_price, is_active)
    VALUES (:hall_id, :amenity_id, :custom_price, :is_active)
    """
    db.execute(text(insert_sql), {
        "hall_id": hall_id,
        "amenity_id": amenity_link.amenity_id,
        "custom_price": amenity_link.custom_price,
        "is_active": amenity_link.is_active,
    })
    db.commit()

    # Return a response shaped like HallAmenityResponse. DB lacks a surrogate id, so expose amenity_id as `id`.
    return {
        "id": amenity_link.amenity_id,
        "hall_id": hall_id,
        "amenity_id": amenity_link.amenity_id,
        "custom_price": amenity_link.custom_price,
        "is_active": amenity_link.is_active,
    }


@router.get("/hall/{hall_id}", response_model=List[HallAmenityResponse])
def get_hall_amenities(
    hall_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    # Use a join query returning amenity details to avoid relying on ORM mapping
    db_hall = db.query(Hall).filter(Hall.hall_id == hall_id).first()
    if not db_hall:
        raise HTTPException(status_code=404, detail="Hall not found")

    # Use raw SQL to avoid referencing missing columns on the HallAmenity model.
    sql = """
    SELECT ha.hall_id, ha.amenity_id, ha.custom_price, ha.is_active, a.amenity_name, a.is_chargeable, a.base_price
    FROM hall_amenities ha
    JOIN amenities a ON a.amenity_id = ha.amenity_id
    WHERE ha.hall_id = :hall_id
    """
    rows = db.execute(text(sql), {"hall_id": hall_id}).mappings().all()

    result = []
    for r in rows:
        # r is a mapping; map fields to expected response shape
        result.append({
            "id": r.get("amenity_id"),
            "hall_id": r.get("hall_id"),
            "amenity_id": r.get("amenity_id"),
            "custom_price": r.get("custom_price"),
            "is_active": bool(r.get("is_active")),
            "amenity_name": r.get("amenity_name"),
            "is_chargeable": bool(r.get("is_chargeable")),
            "base_price": r.get("base_price"),
        })

    return result


@router.put("/hall/{amenity_link_id}/price", response_model=HallAmenityResponse)
def update_hall_amenity_price(
    amenity_link_id: int,
    price_update: dict,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    user_id = int(payload.get("sub"))
    role = payload.get("role")
    
    # The frontend currently treats the returned `id` as the amenity_id.
    amenity_id = amenity_link_id

    # Find the hall_amenity row belonging to a hall the user owns (or superadmin)
    find_sql = """
    SELECT ha.hall_id, ha.amenity_id, ha.custom_price, ha.is_active
    FROM hall_amenities ha
    JOIN halls h ON h.hall_id = ha.hall_id
    WHERE ha.amenity_id = :amenity_id AND h.subadmin_id = :user_id
    """
    row = db.execute(text(find_sql), {"amenity_id": amenity_id, "user_id": user_id}).mappings().first()
    if not row and role != "superadmin":
        raise HTTPException(status_code=404, detail="Hall amenity not found")

    # If superadmin, try to find any matching row without subadmin constraint
    if not row and role == "superadmin":
        row = db.execute(text("SELECT hall_id, amenity_id, custom_price, is_active FROM hall_amenities WHERE amenity_id = :amenity_id"), {"amenity_id": amenity_id}).mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Hall amenity not found")

    # Validate and apply update
    if "custom_price" in price_update:
        # Allow null to reset to base price (set custom_price = NULL)
        if price_update["custom_price"] is None:
            update_sql = """
            UPDATE hall_amenities SET custom_price = NULL
            WHERE hall_id = :hall_id AND amenity_id = :amenity_id
            """
            db.execute(text(update_sql), {"hall_id": row.get("hall_id"), "amenity_id": amenity_id})
            db.commit()
        else:
            if price_update["custom_price"] <= 0:
                raise HTTPException(status_code=400, detail="Price must be greater than 0")
            update_sql = """
            UPDATE hall_amenities SET custom_price = :custom_price
            WHERE hall_id = :hall_id AND amenity_id = :amenity_id
            """
            db.execute(text(update_sql), {"custom_price": price_update["custom_price"], "hall_id": row.get("hall_id"), "amenity_id": amenity_id})
            db.commit()

    # Return the updated shape
    return {
        "id": amenity_id,
        "hall_id": row.get("hall_id"),
        "amenity_id": amenity_id,
        "custom_price": price_update.get("custom_price") if "custom_price" in price_update else row.get("custom_price"),
        "is_active": row.get("is_active"),
    }


@router.delete("/hall/{amenity_link_id}")
def remove_amenity_from_hall(
    amenity_link_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    user_id = int(payload.get("sub"))
    role = payload.get("role")
    
    amenity_id = amenity_link_id

    # Find the row for this amenity that belongs to a hall owned by the user
    find_sql = """
    SELECT ha.hall_id, ha.amenity_id, ha.is_active
    FROM hall_amenities ha
    JOIN halls h ON h.hall_id = ha.hall_id
    WHERE ha.amenity_id = :amenity_id AND h.subadmin_id = :user_id
    """
    row = db.execute(text(find_sql), {"amenity_id": amenity_id, "user_id": user_id}).mappings().first()
    if not row and role != "superadmin":
        raise HTTPException(status_code=404, detail="Hall amenity not found")

    if not row and role == "superadmin":
        row = db.execute(text("SELECT hall_id, amenity_id, is_active FROM hall_amenities WHERE amenity_id = :amenity_id"), {"amenity_id": amenity_id}).mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Hall amenity not found")

    update_sql = """
    UPDATE hall_amenities SET is_active = FALSE
    WHERE hall_id = :hall_id AND amenity_id = :amenity_id
    """
    db.execute(text(update_sql), {"hall_id": row.get("hall_id"), "amenity_id": amenity_id})
    db.commit()

    return {"message": "Amenity removed from hall"}
