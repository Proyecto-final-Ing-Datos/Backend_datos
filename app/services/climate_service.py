from typing import List, Dict
from app.models import ClimateData

# Servicio para obtener estadísticas de datos climáticos
def calculate_statistics(data: List[ClimateData]) -> Dict:
    """
    Calcula estadísticas básicas (mínimo, máximo, promedio) para temperatura, humedad y presión.

    Args:
        data (List[ClimateData]): Lista de datos climáticos.

    Returns:
        dict: Diccionario con estadísticas calculadas.

    Raises:
        ValueError: Si la lista de datos está vacía.
    """
    if not data:
        raise ValueError("La lista de datos climáticos está vacía.")

    try:
        temperature_stats = _calculate_column_statistics([d.temperature for d in data])
        humidity_stats = _calculate_column_statistics([d.humidity for d in data])
        pressure_stats = _calculate_column_statistics([d.pressure for d in data])

        return {
            "count": len(data),
            "temperature": temperature_stats,
            "humidity": humidity_stats,
            "pressure": pressure_stats,
        }
    except Exception as e:
        raise RuntimeError(f"Error al calcular estadísticas: {e}")

def _calculate_column_statistics(column_data: List[float]) -> Dict:
    """
    Calcula estadísticas básicas (mínimo, máximo, promedio) para una columna de datos.

    Args:
        column_data (List[float]): Lista de valores numéricos.

    Returns:
        dict: Diccionario con estadísticas calculadas.
    """
    if not column_data:
        return {"min": None, "max": None, "average": None}

    return {
        "min": min(column_data),
        "max": max(column_data),
        "average": sum(column_data) / len(column_data),
    }
