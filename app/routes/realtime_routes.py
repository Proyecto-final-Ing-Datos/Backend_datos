from fastapi import APIRouter, WebSocket
import asyncio
from app.services.thingspeak_service import fetch_data_from_thingspeak

router = APIRouter()

@router.websocket("/realtime")
async def websocket_endpoint(websocket: WebSocket):
    """
    Envia datos en tiempo real al cliente usando WebSocket.
    """
    await websocket.accept()

    while True:
        df, _ = fetch_data_from_thingspeak()
        if not df.empty:
            await websocket.send_json(df.to_dict(orient="records"))
        await asyncio.sleep(10)  # Actualizar cada 10 segundos
