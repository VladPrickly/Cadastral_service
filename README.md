# Описание
API - сервис, который принимает запрос с указанием кадастрового номера, широты и долготы, эмулирует отправку запроса 
на внешний сервер, и может обрабатывать запрос до 60 секунд. Затем должен отдавать результат запроса. 
Внешний сервер может ответить true или false.

Данные запроса на сервер и ответ с внешнего сервера сохранены в БД. 

Сервис содержит следующие эндпоинты:
 - "/query" - принимает кадастровый номер
 - "/ping" - проверка, что  сервер запустился
 - "/history" - для получения истории запросов
 - "/result" - эндпоинт эмулируемоего сервера, который возвращает true или false
 - "/docs" - документация Swagger для тестирования API
 - "/redoc" - документация ReDoc для тестирования API

## Предварительные требования
- Python 3.12+
- Git
- Docker и Docker Compose
- Доступ к интернету

## Структура проекта
  ```
  cadastral_service/
  ├── app/
  │   ├── __init__.py
  │   ├── config.py
  │   ├── db.py
  │   ├── lifespan.py
  │   ├── main.py
  │   ├── models.py
  │   └── schemas.py
  ├── README.md
  ├── .env
  ├── .gitignore
  ├── requirements.txt
  ├── Dockerfile
  └── docker-compose.yml
  ```

## Установка и удаление
1. Создайте виртуальное окружение:
- Windows:
  ```
  python -m venv .venv
  ```
- Linux/macOS:
  ```
  python3 -m venv .venv
  ```

2. Активируйте виртуальное окружение:
- Windows:
  ```
  venv\Scripts\activate
  ```
- Linux/macOS:
  ```
  source venv/bin/activate
  ```

3. Запуск приложения и создание БД:
  ```
  docker-compose up --build
  ```

4. Остановка приложения:
  ```
  docker-compose down
  ```

5. Удаление контейнеров и томов:
  ```
  docker-compose down -v
  ```

## Проверка работы
  ```
  curl http://localhost:8000/ping
  Ответ: 
  {"status":"ok"}
  ```

  ```
  curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"cadastral_number": "77:01:1234567:890", "latitude": 56.78, "longitude": 43.21}'
  Ответ:
  {
    "id": 1,
    "cadastral_number": "77:01:1234567:890",
    "latitude": 56.78,
    "longitude": 43.21,
    "result": true,
    "created_at": "2026-07-27T21:34:56.789Z"
  }
  ```

  ```
  curl http://localhost:8000/result
  Ответ:
  {"result":true}
  ```

  ```
  curl http://localhost:8000/history
  ```