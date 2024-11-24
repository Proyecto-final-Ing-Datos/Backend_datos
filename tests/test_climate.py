from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_climate_data():
    response = client.post("/api/climate/", json={
        "timestamp": "2024-11-24T12:00:00",
        "temperature": 25.5,
        "humidity": 60,
        "pressure": 1013,
        "location": "Trujillo"
    })
    assert response.status_code == 200
    assert response.json()["temperature"] == 25.5
