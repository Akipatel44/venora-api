from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.service import Service
from app.models.hall_service import HallService
from app.models.hall import Hall
from app.schemas.service import ServiceCreate, ServiceResponse, HallServiceCreate, HallServiceResponse
from app.dependencies import get_current_user_token, role_required


router = APIRouter(prefix="/services", tags=["services"])


@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(
    service_in: ServiceCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(role_required("superadmin")),
):
    db_service = Service(
        service_name=service_in.service_name,
        service_type=service_in.service_type,
        base_price=service_in.base_price,
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


@router.get("/", response_model=List[ServiceResponse])
def get_all_services(
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    services = db.query(Service).all()
    return services


@router.post("/hall/{hall_id}", response_model=HallServiceResponse, status_code=status.HTTP_201_CREATED)
def add_service_to_hall(
    hall_id: int,
    service_link: HallServiceCreate,
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
    
    db_service = db.query(Service).filter(Service.service_id == service_link.service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    existing = db.query(HallService).filter(
        HallService.hall_id == hall_id,
        HallService.service_id == service_link.service_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Service already added to hall")
    
    db_hall_service = HallService(
        hall_id=hall_id,
        service_id=service_link.service_id,
        custom_price=service_link.custom_price,
        is_active=service_link.is_active,
    )
    db.add(db_hall_service)
    db.commit()
    db.refresh(db_hall_service)
    return db_hall_service


@router.get("/hall/{hall_id}", response_model=List[HallServiceResponse])
def get_hall_services(
    hall_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    db_hall = db.query(Hall).filter(Hall.hall_id == hall_id).first()
    if not db_hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    
    services = db.query(HallService).filter(HallService.hall_id == hall_id).all()
    return services


@router.put("/hall/{service_link_id}/price", response_model=HallServiceResponse)
def update_hall_service_price(
    service_link_id: int,
    price_update: dict,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    user_id = int(payload.get("sub"))
    role = payload.get("role")
    
    db_hall_service = db.query(HallService).filter(HallService.id == service_link_id).first()
    if not db_hall_service:
        raise HTTPException(status_code=404, detail="Hall service not found")
    
    db_hall = db.query(Hall).filter(Hall.hall_id == db_hall_service.hall_id).first()
    if db_hall.subadmin_id != user_id and role != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized to modify this hall")
    
    if "custom_price" in price_update and price_update["custom_price"] is not None:
        if price_update["custom_price"] <= 0:
            raise HTTPException(status_code=400, detail="Price must be greater than 0")
        db_hall_service.custom_price = price_update["custom_price"]
    
    db.commit()
    db.refresh(db_hall_service)
    return db_hall_service


@router.delete("/hall/{service_link_id}")
def remove_service_from_hall(
    service_link_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_token),
):
    user_id = int(payload.get("sub"))
    role = payload.get("role")
    
    db_hall_service = db.query(HallService).filter(HallService.id == service_link_id).first()
    if not db_hall_service:
        raise HTTPException(status_code=404, detail="Hall service not found")
    
    db_hall = db.query(Hall).filter(Hall.hall_id == db_hall_service.hall_id).first()
    if db_hall.subadmin_id != user_id and role != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized to modify this hall")
    
    db_hall_service.is_active = False
    db.commit()
    
    return {"message": "Service removed from hall"}
