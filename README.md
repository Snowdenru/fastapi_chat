# WebSocket Chat на FastAPI

Простой веб-чат с использованием FastAPI и WebSocket с красивым интерфейсом на Bootstrap 5.

## Особенности

- Реальное время обмена сообщениями через WebSocket
- Запрос имени пользователя при первом подключении
- Уведомления о подключении/отключении пользователей
- Адаптивный интерфейс на Bootstrap 5
- Сохранение ID пользователя между сессиями

## Требования

- Python 3.7+
- FastAPI
- Uvicorn
- Jinja2

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/snowdenru/fastapi_chat.git
cd fastapi_chat
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите сервер:
```bash
uvicorn main:app --reload
```

## Структура проекта

```
fastapi_chat/
├── main.py              # Основной файл приложения
├── static/              # Статические файлы (CSS, JS)
├── templates/           # HTML шаблоны
│   └── index.html       # Главная страница чата
├── requirements.txt     # Зависимости
└── README.md            # Этот файл
```

## Использование

1. Откройте в браузере: `http://localhost:8000/`
2. При первом посещении введите ваше имя
3. Начните общаться в реальном времени

## API Endpoints

- `GET /` - Главная страница чата
- `GET /generate_id` - Генерация уникального ID клиента
- `WS /ws/{client_id}` - WebSocket endpoint для обмена сообщениями

## Скриншоты



## Лицензия

MIT License

 