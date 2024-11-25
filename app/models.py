from sqlalchemy import Column, Integer, String, Float
from app.db import Base

class ClimateData(Base):
    __tablename__ = "climate_data"
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    timestamp = Column(String, index=True, nullable=False)
