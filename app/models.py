from sqlalchemy import Column, Integer, String, Float
from app.db import Base

class ClimateData(Base):
    __tablename__ = "climate_data"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    timestamp = Column(String, index=True)
