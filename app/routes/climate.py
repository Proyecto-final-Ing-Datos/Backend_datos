from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import ClimateData
from app.models import ClimateData as ClimateDataModel

router = APIRouter()

# Obtener datos climáticos
@router.get("/")
def get_climate_data(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ClimateData).offset(skip).limit(limit).all()

# Insertar un nuevo dato climático
@router.post("/")
def create_climate_data(data: ClimateDataModel, db: Session = Depends(get_db)):
    db_data = ClimateData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
