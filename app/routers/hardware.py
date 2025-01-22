from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import create_hardware_data, get_average_by_set_id
from app.schemas import HardwareDataCreate, HardwareDataResponse

router = APIRouter()

@router.post("/add/", response_model=HardwareDataResponse)
def add_hardware_data(hardware_data: HardwareDataCreate, db: Session = Depends(get_db)):
    return create_hardware_data(db, hardware_data)

@router.get("/{set_id}", response_model=HardwareDataResponse)
def read_hardware_data(set_id: str, db: Session = Depends(get_db)):
    data = get_average_by_set_id(db, set_id)
    if not data:
        raise HTTPException(status_code=404, detail="Hardware data not found")
    return data
