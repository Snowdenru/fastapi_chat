import os
import uuid
from typing import Dict

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Настройка путей
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
templates_dir = os.path.join(current_dir, "templates")

# Подключение статики и шаблонов
app.mount("/static", StaticFiles(directory=static_dir), name='static')
templates = Jinja2Templates(directory=templates_dir)

# Хранилище данных
active_connections: Dict[str, WebSocket] = {}
user_names: Dict[str, str] = {}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websoket: WebSocket, client_id: str):
    await websoket.accept()

    await websoket.send_json({"type": "request_name"})
    name_data = await websoket.receive_json()
    user_name = name_data.get("name", f"User-{client_id[:4]}")
    user_names[client_id] = user_name

    active_connections[client_id] = websoket

    for connection in active_connections.values():
        await connection.send_json({
            "type": "notification",
            "message": f"{user_name} присоединился к чату",
            "color": "success"
        })

    try:
        while True:
            data = await websoket.receive_json()

            if data["type"] == "message":
                message = data["message"]

                for connection in active_connections.values():
                    await connection.send_json({
                        "type": "message",
                        "sender": user_name,
                        "sender_id": client_id,
                        "message": message,
                        "timestamp": data.get("timestamp")
                    })
    except WebSocketDisconnect:
        if client_id in active_connections:
            del active_connections[client_id]
        if client_id in user_names:
            user_name = user_names[client_id]
            del user_names[client_id]
        for connection in active_connections.values():
            await connection.send_json({
                "type": "notification",
                "message": f"{user_name} покинул чат",
                "color": "warning"
            })







@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/generate_id")
async def generate_id():
    return {"client_id": str(uuid.uuid4())}

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)