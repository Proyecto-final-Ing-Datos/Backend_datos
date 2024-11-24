from typing import List
from app.models import ClimateData

# Servicio para obtener estadísticas de datos climáticos
def calculate_statistics(data: List[ClimateData]):
    return {
        "count": len(data),
        "temperature": {
            "min": min(d.temperature for d in data),
            "max": max(d.temperature for d in data),
            "average": sum(d.temperature for d in data) / len(data),
        },
        "humidity": {
            "min": min(d.humidity for d in data),
            "max": max(d.humidity for d in data),
            "average": sum(d.humidity for d in data) / len(data),
        },
        "pressure": {
            "min": min(d.pressure for d in data),
            "max": max(d.pressure for d in data),
            "average": sum(d.pressure for d in data) / len(data),
        },
    }
