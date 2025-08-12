# Разбор работы WebSocket эндпоинта для чата

Этот код реализует серверную часть WebSocket-чата с использованием FastAPI. Давайте разберём его работу пошагово:

## 1. Объявление эндпоинта
```python
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
```
- `@app.websocket("/ws/{client_id}")` - декоратор, создающий WebSocket эндпоинт по указанному пути
- `client_id` - уникальный идентификатор клиента, передаваемый в URL

## 2. Принятие соединения
```python
await websocket.accept()
```
- Сервер принимает входящее WebSocket-соединение

## 3. Запрос имени пользователя
```python
await websocket.send_json({"type": "request_name"})
name_data = await websocket.receive_json()
user_name = name_data.get("name", f"User-{client_id[:4]}")
user_names[client_id] = user_name
```
- Сервер отправляет клиенту запрос на предоставление имени (`request_name`)
- Ожидает ответ от клиента в формате JSON
- Извлекает имя из ответа или использует имя по умолчанию (User-XXXX, где XXXX - первые 4 символа client_id)
- Сохраняет имя пользователя в словаре `user_names`

## 4. Регистрация соединения
```python
active_connections[client_id] = websocket
```
- Добавляет текущее соединение в словарь активных соединений `active_connections`

## 5. Уведомление о новом пользователе
```python
for connection in active_connections.values():
    await connection.send_json({
        "type": "notification",
        "message": f"{user_name} присоединился к чату",
        "color": "success"
    })
```
- Рассылает всем подключённым клиентам уведомление о новом пользователе
- Сообщение содержит тип (`notification`), текст и цвет (для отображения на клиенте)

## 6. Основной цикл обработки сообщений
```python
try:
    while True:
        data = await websocket.receive_json()
        
        if data["type"] == "message":
            message = data["message"]
            # Отправляем сообщение всем
            for conn_id, connection in active_connections.items():
                await connection.send_json({
                    "type": "message",
                    "sender": user_name,
                    "sender_id": client_id,
                    "message": message,
                    "timestamp": data.get("timestamp")
                })
```
- Бесконечный цикл ожидания сообщений от клиента
- При получении сообщения (`type: "message"`) рассылает его всем подключённым клиентам
- Каждое сообщение содержит:
  - Тип (`message`)
  - Имя отправителя
  - ID отправителя
  - Текст сообщения
  - Временную метку

## 7. Обработка отключения клиента
```python
except WebSocketDisconnect:
    if client_id in active_connections:
        del active_connections[client_id]
    if client_id in user_names:
        user_name = user_names[client_id]
        del user_names[client_id]
        # Уведомляем о выходе пользователя
        for connection in active_connections.values():
            await connection.send_json({
                "type": "notification",
                "message": f"{user_name} покинул чат",
                "color": "warning"
            })
```
- При разрыве соединения (исключение `WebSocketDisconnect`):
  - Удаляет соединение из словаря активных соединений
  - Удаляет имя пользователя из словаря имён
  - Рассылает уведомление о выходе пользователя

## Глобальные структуры данных
Код предполагает наличие где-то в модуле двух словарей:
```python
active_connections = {}  # Хранит активные соединения (client_id: WebSocket)
user_names = {}          # Хранит имена пользователей (client_id: user_name)
```

## Протокол обмена сообщениями
Сервер использует JSON-сообщения с полем `type`, которое определяет тип сообщения:
1. `request_name` - запрос имени пользователя
2. `notification` - уведомление (о входе/выходе пользователя)
3. `message` - обычное сообщение чата

Этот код обеспечивает базовую функциональность чата: регистрацию пользователей, обмен сообщениями и уведомления о подключении/отключении участников.