from pydantic import BaseModel
from datetime import datetime

# Modelo Pydantic para los datos climáticos
class ClimateData(BaseModel):
    timestamp: datetime
    temperature: float
    humidity: float
    pressure: float
    location: str
